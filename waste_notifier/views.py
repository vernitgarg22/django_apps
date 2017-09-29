import requests
import datetime

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Subscriber
from waste_schedule.models import ScheduleDetail

from waste_notifier.util import *
import cod_utils.util
import cod_utils.security
from cod_utils.messaging import MsgHandler
from cod_utils.cod_logger import CODLogger

import direccion


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
    address = direccion.Address(street_address)
    location = address.geocode()

    # TODO figure out how to handle 'address not found' or 'no address supplied'
    if not location or location['score'] < 50:

        MsgHandler().send_admin_alert('Invalid waste reminder text signup: {}'.format(street_address))

        msg = "Unfortunately, address {} could not be located - please text the street address only, for example '1301 3rd ave'".format(street_address)
        text_signup_number = settings.AUTO_LOADED_DATA["WASTE_REMINDER_TEXT_SIGNUP_NUMBERS"][0]
        MsgHandler().send_text(phone_number=phone_number, phone_sender=text_signup_number, text=msg)

        return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Now look up waste areas for this location
    GIS_ADDRESS_LOOKUP_URL = "https://gis.detroitmi.gov/arcgis/rest/services/DPW/All_Services/MapServer/0/query?where=&text=&objectIds=&time=&geometry={}%2C+{}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelWithin&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=json"
    url = GIS_ADDRESS_LOOKUP_URL.format(location['location']['x'], location['location']['y'])
    response = requests.get(url)

    waste_area_ids = [ feature['attributes']['FID'] for feature in response.json()['features'] ]

    # Create the subscriber and activate them
    subscriber, error = Subscriber.update_or_create_from_dict( { "phone_number": phone_number, "waste_area_ids": waste_area_ids } )
    if error:    # pragma: no cover (should never get here)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    add_subscriber_comment(phone_number=phone_number, comment='signed up via text')
    return update_subscription(phone_number, True)


def update_subscription(phone_number, activate):
    """
    Find the subscriber and activate / deactivate them
    """

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

    return Response({ "subscriber": str(subscriber), "message": body }, status=status.HTTP_201_CREATED)


def add_subscriber_comment(phone_number, comment):
    subscribers = Subscriber.objects.filter(phone_number__exact=phone_number)
    if not subscribers.exists():
        return     # pragma: no cover (should never get here)

    subscriber = subscribers[0]
    if subscriber.comment:
        comment = subscriber.comment + ' - ' + comment

    subscriber.comment = comment
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
    remove_me = "remove me" in body
    response = {}

    # Update user status
    if "remove me" in body:
        response = update_subscription(phone_number, False)
    else:
        response = update_subscription(phone_number, True)

    add_subscriber_comment(phone_number, "User's response to confirmation was: {}".format(body))
    return response


@api_view(['POST'])
def send_notifications(request, date_val=cod_utils.util.tomorrow(), date_name=None, format=None):
    """
    Send out any necessary notifications (e.g., regular schedule or schedule changes)
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if cod_utils.security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        MsgHandler().send_admin_alert("Address {} was blocked from sending waste alerts".format(remote_addr))
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Throw error if there is an unrecognized query param
    for param in request.query_params.keys():
        if param not in ['dry_run', 'today']:
            return Response("Invalid param: " + param, status=status.HTTP_400_BAD_REQUEST)

    # Allow caller to pass in dry_run flag
    dry_run_param = request.query_params.get('dry_run') == 'true'

    # Allow caller to specify what 'today' is
    today = request.query_params.get('today')
    if today and date_name:
        return Response("Do not supply both today and date name", status=status.HTTP_400_BAD_REQUEST)

    if today:
        date_val = cod_utils.util.tomorrow(today)
    elif date_name == 'tomorrow':
       date_val = cod_utils.util.tomorrow()

    date = date_val
    if type(date) is str:
        date = datetime.date(int(date_val[0:4]), int(date_val[4:6]), int(date_val[6:8]))

    subscribers_services = SubscriberServices()
    subscribers_services_details = []

    # loop through all routes for the day
    routes = ScheduleDetailMgr.instance().get_day_routes(date)
    for route_id, route in routes.items():

        service_type = ScheduleDetail.map_service_type(route['services'])
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

            # TODO disable this temporarily
            MsgHandler().send_text(phone_number=subscriber.phone_number, text=message, dry_run_param=dry_run_param)

    content = NotificationContent(subscribers_services, subscribers_services_details, date, dry_run_param or settings.DRY_RUN)

    # slack the json response to #zzz
    slack_alerts_summary(content.get_content())

    return Response(content.get_content())


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
