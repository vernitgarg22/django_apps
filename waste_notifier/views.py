import requests
from datetime import datetime

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
    return "Your next upcoming pickup for {0} is {1}".format(get_services_desc(services), date.strftime("%b %d, %Y"))


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


@api_view(['GET'])
def send_notifications(request, date=datetime.today(), format=None):
    """
    Send out any necessary notifications (e.g., regular schedule or schedule changes)
    """

    if type(date) is str:
        date = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    content = {}

    subscribers_map = {}
    notifications = {}

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

            # keep track of what services each subscriber needs notifications for
            for subscriber in subscribers:
                subscribers_map[subscriber.phone_number] = subscriber
                services = notifications.get(subscriber.phone_number) or []
                services.extend([service_type])
                notifications[subscriber.phone_number] = services

            # TODO: factor in schedule changes
            # TODO: factor in notifications

    # send text reminder to each subscriber needing a reminder
    for phone_number in list(notifications.keys()):
        subscriber = subscribers_map[phone_number]
        client.messages.create(
            to = "+1" + subscriber.phone_number,
            from_ = PHONE_SENDER,
            body = get_service_message(notifications[phone_number], date),
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
