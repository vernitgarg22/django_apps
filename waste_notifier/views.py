import requests
import datetime
from datetime import date

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Subscriber
from waste_schedule.models import ScheduleDetail

from waste_notifier.util import *
from waste_schedule.util import *
import cod_utils.util
import cod_utils.security
from cod_utils.util import date_json
from cod_utils.messaging import MsgHandler
from cod_utils.cod_logger import CODLogger

from waste_schedule.models import ScheduleDetail


@api_view(['POST'])
def subscribe_notifications(request):
    """
    Parse subscription request and text user request for confirmation
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if cod_utils.security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        MsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # update existing subscriber or create new one from data
    subscriber, error = Subscriber.update_or_create_from_dict(request.data)
    if error:
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    # add description of desired list of services to response
    services = add_additional_services(util.split_csv(subscriber.service_type), date=None, add_yard_waste_year_round=True)
    services_desc = get_services_desc(services)
    body = "City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive {} pickup reminders"
    body = body.format(services_desc)

    add_subscriber_comment(subscriber=subscriber, comment='signed up via web')

    # text the subscriber to ask them to confirm
    MsgHandler().send_text(phone_number=subscriber.phone_number, text=body)

    return Response({ "received": str(subscriber), "message": body }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def subscribe_address(request):
    """
    Parse subscription request via text message with user's street address and text user request for confirmation.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    msg_handler = MsgHandler()

    # Make sure the call came from twilio and is valid
    msg_handler.validate(request)

    # Verify required fields are present
    if not request.data.get('From') or not request.data.get('Body'):
        return Response({"error": "From and body values are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Clean up phone number
    phone_number = msg_handler.get_fone_number(request)

    street_address = request.data.get('Body').upper().strip()

    pos = street_address.find("DETROIT")
    if pos >= 0:
        street_address = street_address[0:pos]

    # Parse address string and get result from AddressPoint geocoder
    location, address = geocode_address(street_address=street_address)
    if not location:
        invalid_addr_msg = 'Invalid waste reminder text signup: {} from {}'.format(street_address, phone_number)

        CODLogger.instance().log_error(name=__name__, area="waste notifier signup by text", msg=invalid_addr_msg)

        MsgHandler().send_admin_alert(invalid_addr_msg)

        msg = "Unfortunately, address {} could not be located - please text the street address only, for example '1301 3rd ave'".format(street_address)
        text_signup_number = settings.AUTO_LOADED_DATA["WASTE_REMINDER_TEXT_SIGNUP_NUMBERS"][0]
        MsgHandler().send_text(phone_number=phone_number, phone_sender=text_signup_number, text=msg)

        return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)

    waste_area_ids = get_waste_area_ids(location=location)

    # Create the subscriber and activate them
    subscriber, error = Subscriber.update_or_create_from_dict( { "phone_number": phone_number, "waste_area_ids": waste_area_ids, "address": address.address, "latitude": location['location']['y'], "longitude": location['location']['x'] } )
    if error:
        return Response(error, status=status.HTTP_400_BAD_REQUEST)    # pragma: no cover (should never get here)

    add_subscriber_comment(subscriber=subscriber, comment='signed up via text')
    subscriber, response = update_subscription(phone_number=phone_number, activate=True, subscriber=subscriber)
    return response


def update_subscription(phone_number, activate, subscriber=None):
    """
    Find the subscriber and activate / deactivate them
    """

    if not subscriber:
        subscribers = Subscriber.objects.filter(phone_number__exact=phone_number)
        if not subscribers.exists():
            raise Http404("Subscriber not found")

        subscriber = subscribers[0]

    subscriber.activate() if activate else subscriber.deactivate()

    # Get proper response
    body = ''
    if activate:
        body = "City of Detroit Public Works:  your {0} pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)"
    else:
        body = "City of Detroit Public Works:  your {0} pickup reminders have been cancelled (reply to this message at any time with ADD ME to start receiving reminders again)"

    # add description of desired list of services to response
    services = add_additional_services(util.split_csv(subscriber.service_type), date=None, add_yard_waste_year_round=True)
    services_desc = get_services_desc(services)
    body = body.format(services_desc)

    # send the subscriber a confirmation message
    MsgHandler().send_text(phone_number=subscriber.phone_number, text=body)

    return subscriber, Response({ "subscriber": str(subscriber), "message": body }, status=status.HTTP_201_CREATED)


def add_subscriber_comment(subscriber, comment):
    """
    Update / add comment to the subscriber.
    """

    # Build new comment at end of any previous comments
    new_comment = subscriber.comment + ' - ' + comment if subscriber.comment else comment

    # Truncate if necessary.
    if len(new_comment) >= Subscriber._meta.get_field('comment').max_length:
        new_comment = "(previous comments truncated) ... " + comment

    # Save new comment
    subscriber.comment = new_comment
    subscriber.clean()
    subscriber.save()


@api_view(['POST'])
def confirm_notifications(request):
    """
    Parse subscription confirmation and send a simple response
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    msg_handler = MsgHandler()

    # Make sure the call came from twilio and is valid
    msg_handler.validate(request)

    # Verify required fields are present
    if not request.data.get('From') or not request.data.get('Body'):
        return Response({"error": "From and body values are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Clean up phone number
    phone_number = msg_handler.get_fone_number(request)

    body = request.data['Body']
    body = body.lower()

    # unless user wants to be removed, add them
    add_me = "remove me" not in body
    response = {}

    # Update user status
    subscriber, response = update_subscription(phone_number=phone_number, activate=add_me)

    add_subscriber_comment(subscriber=subscriber, comment="User's response to confirmation was: {}".format(body))
    return response


def send_notifications_request(date_val=cod_utils.util.tomorrow(), date_name=None, today=None, format=None, dry_run_param=False):
    """
    Send out any necessary notifications (e.g., regular schedule or schedule changes)
    """

    # Allow caller to specify what 'today' is
    if today and date_name:
        return Exception("Do not supply both today and date name")

    if today:
        date_val = cod_utils.util.tomorrow(today)
    elif date_name == 'tomorrow':
       date_val = cod_utils.util.tomorrow()

    return send_notifications(date_val, dry_run_param)


def send_notifications(date, dry_run_param=False):

    if type(date) is str:
        date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))

    if settings.DRY_RUN:
        dry_run_param = True

    subscribers_services = SubscriberServices()
    subscribers_services_details = []

    # loop through all routes for the day
    routes = ScheduleDetailMgr.instance().get_day_routes(date)
    for route_id, route in routes.items():

        service_type = map_service_type(route['services'])
        if service_type == ScheduleDetail.ALL:
            service_type = ScheduleDetailMgr.instance().check_all_service_week(date, route)

        subscribers = get_route_subscribers(service_type, route_id)

        # keep track of what services each subscriber needs notifications for
        subscribers_services.add(subscribers, service_type, [route_id])

    # Check if there are any schedule details for this date
    schedule_details = ScheduleDetailMgr.instance().get_schedule_details(date)
    for detail in schedule_details:

        subscribers_services_detail = SubscriberServicesDetail(detail, detail.service_type, '')

        detail_subscribers = get_subscribers(detail, date)

        # Find anyone subscribed to any of the services for this schedule detail
        if detail_subscribers.get(ScheduleDetail.ALL):
            subscribers_services_detail.add(detail_subscribers[ScheduleDetail.ALL], ScheduleDetail.ALL, detail.waste_area_ids)
        else:
            for service_type in detail_subscribers.keys():
                subscribers_services_detail.add(detail_subscribers[service_type], service_type, detail.waste_area_ids)

        subscribers_services_details.append(subscribers_services_detail)

    # send text reminder to each subscriber needing a reminder
    for subscriber in subscribers_services.get_subscribers():

        message = get_service_message(subscribers_services.get_services(subscriber), date)
        MsgHandler().send_text(phone_number=subscriber.phone_number, text=message, dry_run_param=dry_run_param)

    # send out notifications about any schedule changes
    for subscribers_services_detail in subscribers_services_details:
        for subscriber in subscribers_services_detail.get_subscribers():

            message = get_service_detail_message(subscribers_services_detail.get_services(subscriber), subscribers_services_detail.schedule_detail)

            MsgHandler().send_text(phone_number=subscriber.phone_number, text=message, dry_run_param=dry_run_param)

    content = NotificationContent(subscribers_services, subscribers_services_details, date, dry_run_param)

    # slack the json response to #zzz
    slack_alerts_summary(content.get_content())

    return content.get_content()


@api_view(['GET'])
def get_address_service_info(request, street_address, today = datetime.date.today(), format=None):
    """
    Return service information for a single address.

    Note:
    - the address value can include alphanumeric characters and spaces.
    - the call needs to be https.
    - if the address cannot be matched (or gets a top match that has a score that is too low) an error gets returned.
    """

    # TODO for security, verify call is from alexa / google home app?

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    if type(today) is str:
        today = datetime.datetime.strptime(today, "%Y%m%d")

    tomorrow = util.tomorrow(today)

    # Parse address string and get result from AddressPoint geocoder
    location, address = geocode_address(street_address=street_address)
    if not location:
        invalid_addr_msg = 'Invalid address received in service info request: {}'.format(address)

        CODLogger.instance().log_error(name=__name__, area="service info request", msg=invalid_addr_msg)

        MsgHandler().send_admin_alert(text=invalid_addr_msg)

        return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)

    service_info = get_waste_area_ids(location=location, ids_only=False)

    schedule_changes = ScheduleDetailMgr.instance().get_date_schedule_changes(tomorrow)

    # Add in next pickups for each service
    content = { "next_pickups": {}}
    for info in service_info:

        services = add_additional_services([info['services']], tomorrow)
        for service in services:

            # When is tentative date for next pickup for the service, ignoring
            # holidays and alt weeks, for now?
            diff = get_day_of_week_diff(tomorrow, info['day'])
            next_date = tomorrow + datetime.timedelta(days = diff)

            # Check for alt week
            if service != ScheduleDetail.TRASH:
                if not ScheduleDetail.check_date_service(next_date, BiWeekType.from_str(info['week'])):
                    next_date += datetime.timedelta(days = 7)

            # Check for holiday schedule changes
            schedule_changes = ScheduleDetailMgr.instance().get_date_schedule_changes(next_date)
            if schedule_changes:
                next_date += datetime.timedelta(days = 1)

            # REVIEW: should really pass "-05:00" for add_tz
            content["next_pickups"][map_service_type(service)] =  {
                "date": date_json(next_date, add_tz=False),
                "provider": info['contractor']
            }

    # Add list of all services that currently exist
    content["all_services"] = add_additional_services(services=ScheduleDetail.ALL, date=tomorrow, add_yard_waste_year_round=True)

    # TODO Add in all schedule details for the next month?
    # TODO Use ScheduleDetailMgr.get_week_schedule_changes for this ?

    details_content = {}
    end_date = tomorrow + datetime.timedelta(days=30)
    details = ScheduleDetail.objects.exclude(normal_day__lt=tomorrow).exclude(new_day__lt=tomorrow).exclude(normal_day__gt=end_date).exclude(new_day__gt=end_date)
    for detail in details:
        detail_json = detail.json()
        detail_type = detail_json.pop('type')
        if not details_content.get(detail_type):
            details_content[detail_type] = []
        details_content[detail_type].append(detail_json)

    content["details"] = details_content

    return Response(content)


def get_route_subscribers(service_type, route_id):
    """
    Return all subscribers who are subscribed to the particular service type and route
    """

    # get all active subscribers to this service type
    subscribers = Subscriber.objects.filter(status__exact='active')
    if service_type != ScheduleDetail.ALL:
        subscribers = subscribers.filter(service_type__contains=ScheduleDetail.ALL) | subscribers.filter(service_type__contains=service_type)

    # also filter subscribers by route
    return subscribers.filter(waste_area_ids__contains=',' + str(route_id) + ',')

def filter_route_subscribers(detail, subscribers):
    """
    Filters out subscribers who are not subscribed to this detail's routes
    """

    route_ids = util.split_csv(detail.waste_area_ids)

    # Just return all subscribers if detail is city-wide
    if not route_ids:
        return subscribers

    # Combine subscribers to each route
    dest = Subscriber.objects.none()
    for route_id in route_ids:
        tmp = subscribers.filter(waste_area_ids__contains="," + str(route_id) + ",")
        dest = dest | tmp

    return dest

def map_service_subscribers(detail, subscribers, date):
    """
    Filter out subscribers not subscribed to the given service type(s).  Results get returned
    as a map, which maps from service_type to subscribers for that service.
    """

    if detail.service_type == ScheduleDetail.ALL:
        return { ScheduleDetail.ALL: subscribers }

    # Combine subscribers to each service type
    dest = {}
    for service_type in util.split_csv(detail.service_type):
        tmp = subscribers.filter(service_type__contains=service_type) | subscribers.filter(service_type__exact=ScheduleDetail.ALL)

        service_type_subscribers = [ subscriber for subscriber in tmp if subscriber.has_service_on_date_week(service_type, date) ]
        dest[service_type] = service_type_subscribers

    return dest

def get_subscribers(detail, date):
    """

    current thinking about schedule detail alerts:

    schedule changes
       - on the day when pickups would have occurred (i.e., the normal_day), a notification should go out to all subscribers 
         to the route, or, for city-wide schedule changes, to all active subscribers

    start-date and end-date
       - on the day where the service start or end takes effect (i.e., the new day), a notification should go out to all
         subscribers to the route, or, if this service is starting / ending city-wide, to all active subscribers

    info
       - on the day that the informational detail applies to (i.e., its normal_day), a notification should go out to all subscribers 
         to the route, or, for city-wide schedule changes, to all active subscribers

    """

    # get active subscribers
    subscribers = Subscriber.objects.filter(status__exact='active')

    # get subscribers subscribed to the particular detail routes
    subscribers = filter_route_subscribers(detail, subscribers)

    return map_service_subscribers(detail, subscribers, date)


@api_view(['GET'])
def get_route_info(request, format=None):
    """
    Output information about each waste collection route, grouped by day
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Build list of days -- each day will have a list of routes
    routes_by_day = [ { day: [] } for day in ScheduleDetail.DAYS[:-2] ]

    # Build a list route info objects for all routes
    r = requests.get(ScheduleDetail.GIS_URL_ALL)
    routes = [ { "route": feature['attributes']['FID'], 'services': feature['attributes']['services'], 'day': feature['attributes']['day'], 'week': feature['attributes']['week'], 'contractor': feature['attributes']['contractor'] } for feature in r.json()['features'] ]

    # Loop through the routes, adding each one to the correct day
    for route in routes:
        day = route.pop('day')
        if route['services'] == 'trash':
            del route['week']
        index = ScheduleDetail.DAYS.index(day)
        routes_by_day[index][day].append(route)

    return Response(routes_by_day)
