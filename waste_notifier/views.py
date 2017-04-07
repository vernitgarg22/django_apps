import requests
import datetime

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Subscriber
from waste_schedule.models import ScheduleDetail

from twilio.rest import TwilioRestClient


ACCOUNT_SID = "AC8b444a6aeeb1afdba3c064f2d105057d"
AUTH_TOKEN = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']
PHONE_SENDER = "+13132283402"


def get_services_desc(services):
    """
    Returns comma-delimited list of services, with last comma replaced by 'and'
    """

    # build comma-delimited list of services
    desc = ''.join([ service + ', ' for service in list(set(services)) ])

    # remove trailing comma
    desc = desc[:-2]

    # if more than 1 service, replace last comma with 'and'
    if len(services) > 1:
        index = desc.rfind(',')
        desc = desc[0: index] + " and" + desc[index + 1: ]

    return desc

def get_service_message(services, date):
    """
    Returns message to be sent to subscriber, including correct list of services and date
    """
    return "City of Detroit Public Works:  Your next upcoming pickup for {0} is {1}".format(get_services_desc(services), date.strftime("%b %d, %Y"))


def get_service_detail_message(services, detail):
    """
    Returns message to be sent to subscriber, including correct list of services and informtion about service detail
    (e.g., schedule change)
    """

    message = 'City of Detroit Public Works:  '
    detail_desc = ''
    if detail.detail_type == 'schedule':
        detail_desc = "Your pickup for {0} for {1} is postponed to {2} due to {3}".format(get_services_desc(services), 
            detail.normal_day.strftime("%b %d, %Y"), detail.new_day.strftime("%b %d, %Y"), detail.description)
    elif detail.detail_type == 'info':
        detail_desc = detail.description
    elif detail.detail_type == 'start-date' or detail.detail_type == 'end-date':
        detail_desc = detail.description + ' ' + detail.new_day.strftime("%b %d, %Y")

    message = message + detail_desc
    if detail.note:
        message = message + " - " + detail.note

    return message

@api_view(['POST'])
def subscribe_notifications(request):
    """
    Parse subscription request and text user request for confirmation
    """

    # update existing subscriber or create new one from data
    subscriber, error = Subscriber.update_or_create_from_dict(request.data)
    if error:
        return Response(error)

    # create a twilio client and text the subscriber to ask them to confirm
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        to = "+1" + subscriber.phone_number,
        from_ = PHONE_SENDER,
        body = "City of Detroit Public Works:  reply with YES to confirm that you want to receive trash & recycling pickup reminders",
    )

    # TODO return better response?
    return Response({ "received": str(subscriber) })


@api_view(['POST'])
def confirm_notifications(request):
    """
    Parse subscription confirmation and send a simple response
    """

    # validator = RequestValidator(AUTH_TOKEN)

    # Verify required fields are present
    if not request.data.get('From') or not request.data.get('Body'):
        return Response({"error": "From and body values are required"})

    # Clean up phone number
    phone_number = request.data['From'].replace('+', '')
    if phone_number.startswith('1'):
        phone_number = phone_number[1:]

    # Did user confirm they want to receive notifications?
    body = request.data['Body']
    if body.find("YES") < 0:
        return Response({})

    # Find the subscriber and activate them
    subscribers = Subscriber.objects.filter(phone_number__exact=phone_number)
    if not subscribers.exists():
        raise Http404("Subscriber not found")

    subscriber = subscribers[0]
    subscriber.activate()

    # create a twilio client and send the subscriber a confirmation message
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        to = "+1" + subscriber.phone_number,
        from_ = PHONE_SENDER,
        body = "City of Detroit Public Works:  your trash & recycling pickup reminders have been confirmed\n(reply STOP to any of the reminders to stop receiving them)",
    )

    return Response({ "subscriber": str(subscriber) })


class SubscriberServices:
    """
    Keeps track of what subscribes are supposed to receive a notification
    """

    def __init__(self):
        self.subscribers = {}
        self.services = {}

    def add(self, subscribers, service):
        for subscriber in subscribers:
            self.subscribers[subscriber.phone_number] = subscriber
            services_list = self.services.get(subscriber.phone_number) or []
            services_list.extend([service])
            self.services[subscriber.phone_number] = services_list

    def get_subscribers(self):
        return self.subscribers.values()

    def get_service(self, subscriber):
        return self.services[subscriber.phone_number]


class SubscriberServicesDetail(SubscriberServices):
    """
    Keeps track of what subscribes are supposed to receive a notification
    about a schedule change
    """

    def __init__(self, schedule_detail, subscribers, service):
        super().__init__()
        self.schedule_detail = schedule_detail
        for subscriber in subscribers:
            self.add(subscribers, service)


@api_view(['GET'])
def send_notifications(request, date_val=datetime.date.today(), format=None):
    """
    Send out any necessary notifications (e.g., regular schedule or schedule changes)
    """

    date = date_val
    if type(date) is str:
        date = datetime.date(int(date_val[0:4]), int(date_val[4:6]), int(date_val[6:8]))

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    content = {}

    subscribers_services = SubscriberServices()
    subscribers_services_details = []

    for service_type in list(ScheduleDetail.SERVICE_ID_MAP.keys()):

        # Find out which waste areas are about to get pickups for this service
        routes = ScheduleDetail.get_waste_routes(date, service_type)

        # get a list of route ids
        route_ids = [ int(id) for id in list(routes.keys()) if id ]
        for route_id in route_ids:

            # get all active subscribers to this service ...
            subscribers = Subscriber.objects.using('default').filter(status__exact='active')
            subscribers = subscribers.filter(service_type__contains='all') | subscribers.filter(service_type__contains=service_type)

            # also filter subscribers by route
            subscribers = subscribers.filter(waste_area_ids__contains=',' + str(route_id) + ',')
            content[route_id] = [ subscriber.phone_number for subscriber in subscribers ]

            # does this route have any schedule changes for this date?
            schedule_changes = ScheduleDetail.get_schedule_changes(route_id, date)
            if schedule_changes:
                subscribers_services_details.append(SubscriberServicesDetail(schedule_changes[0], subscribers, service_type))
            else:
                # keep track of what services each subscriber needs notifications for
                subscribers_services.add(subscribers, service_type)

    # send text reminder to each subscriber needing a reminder
    for subscriber in subscribers_services.get_subscribers():
        client.messages.create(
            to = "+1" + subscriber.phone_number,
            from_ = PHONE_SENDER,
            body = get_service_message(subscribers_services.get_service(subscriber), date),
        )

    # send out notifications about any schedule changes
    for subscribers_services_detail in subscribers_services_details:
        for subscriber in subscribers_services_detail.get_subscribers():

            message = get_service_detail_message(subscribers_services_detail.get_service(subscriber), subscribers_services_detail.schedule_detail)
            client.messages.create(
                to = "+1" + subscriber.phone_number,
                from_ = PHONE_SENDER,
                body = message,
            )

    return Response(content)


@api_view(['GET'])
def list_route_info(request, format=None):
    """
    Output information about each waste collection route
    """

    routes_by_day = [ { day: {} } for day in ScheduleDetail.DAYS[:-2] ]
    for service_type in list(ScheduleDetail.SERVICE_ID_MAP.keys()):

        service_id = ScheduleDetail.SERVICE_ID_MAP[service_type]
        for day in ScheduleDetail.DAYS[:-2]:

            url = ScheduleDetail.GIS_URL.format(service_id, day)
            r = requests.get(url)

            routes = [ { "route": feature['attributes']['FID'], 'week': feature['attributes']['week'], 'contractor': feature['attributes']['contractor'] } for feature in r.json()['features'] ]
            index = ScheduleDetail.DAYS.index(day)

            for route in routes:
                route_id = route["route"]
                services_desc = service_type
                if routes_by_day[index][day].get(route_id):
                    services_desc = services_desc + ", " + routes_by_day[index][day][route_id]["services"]
                route["services"] = services_desc
                routes_by_day[index][day][route_id] = route

    return Response(routes_by_day)
