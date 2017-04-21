import requests
import datetime

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Subscriber
from waste_schedule.models import ScheduleDetail

import cod_utils.util
from cod_utils.util import MsgHandler


def get_services_desc(services):
    """
    Returns comma-delimited list of services, with last comma replaced by 'and'.
    Input should be a list of services.
    """

    if services[0] == "all":
        return "waste collection"

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

    # TODO REVIEW make it impossible to call this from outside our network?

    # update existing subscriber or create new one from data
    subscriber, error = Subscriber.update_or_create_from_dict(request.data)
    if error:
        return Response(error)

    # text the subscriber to ask them to confirm
    MsgHandler().send_text(subscriber.phone_number, "City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive trash & recycling pickup reminders")

    return Response({ "received": str(subscriber) })


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
    services_desc = get_services_desc(subscriber.service_type.split(','))
    body = body.format(services_desc)

    # send the subscriber a confirmation message
    MsgHandler().send_text(subscriber.phone_number, body)

    return Response({ "subscriber": str(subscriber) })


@api_view(['POST'])
def confirm_notifications(request):
    """
    Parse subscription confirmation and send a simple response
    """

    # # Make sure the call came from twilio and is valid
    MsgHandler().validate(request)

    # Verify required fields are present
    if not request.data.get('From') or not request.data.get('Body'):
        return Response({"error": "From and body values are required"})

    # Clean up phone number
    phone_number = request.data['From'].replace('+', '')
    if phone_number.startswith('1'):
        phone_number = phone_number[1:]

    # Did user confirm they want to receive notifications?
    body = request.data['Body']
    body = body.strip()

    if body == "ADD ME":
        return update_subscription(phone_number, True)
    elif body == "REMOVE ME":
        return update_subscription(phone_number, False)
    else:
        return Response({})


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


@api_view(['POST'])
def send_notifications(request, date_val=cod_utils.util.tomorrow(), date_name=None, format=None):
    """
    Send out any necessary notifications (e.g., regular schedule or schedule changes)
    """

    # TODO REVIEW make it impossible to call this from outside our network?

    dry_run_param = request.query_params.get('dry_run') == 'true'

    if date_name == 'tomorrow':
       date_val = cod_utils.util.tomorrow()

    date = date_val
    if type(date) is str:
        date = datetime.date(int(date_val[0:4]), int(date_val[4:6]), int(date_val[6:8]))

    # TODO output what type of reminder was sent out:
    # - normal weekly reminder
    # - schedule change
    # - info only notice
    # - start or end date
    content = { "meta": { "date_applicable": str(date), "dry_run": settings.DRY_RUN }, "citywide": {} }

    subscribers_services = SubscriberServices()
    subscribers_services_details = []

    # loop through the different types of service and check for subscribers
    # to each route servicing a service type on the given date
    for service_type in list(ScheduleDetail.SERVICE_ID_MAP.keys()):

        # Find out which waste areas are about to get pickups for this service
        routes = ScheduleDetail.get_waste_routes(date, service_type)

        # get a list of route ids
        route_ids = [ int(id) for id in list(routes.keys()) ]
        for route_id in route_ids:

            # get all active subscribers to this service ...
            subscribers = Subscriber.objects.filter(status__exact='active')
            subscribers = subscribers.filter(service_type__contains='all') | subscribers.filter(service_type__contains=service_type)

            # also filter subscribers by route
            subscribers = subscribers.filter(waste_area_ids__contains=',' + str(route_id) + ',')

            # track, by route, which phone numbers we have texted
            if not content.get(service_type):
                content[service_type] = {}
            content[service_type].update( { route_id: { subscriber.phone_number: 1 for subscriber in subscribers } } )

            # does this route have any schedule changes for this date?
            schedule_details = ScheduleDetail.get_schedule_changes(route_id, date)
            if schedule_details:
                subscribers_services_details.append(SubscriberServicesDetail(schedule_details[0], subscribers, service_type))
            else:
                # keep track of what services each subscriber needs notifications for
                subscribers_services.add(subscribers, service_type)

    # check for schedule details that are city-wide (i.e., not tied to a specific route)
    schedule_details = ScheduleDetail.get_citywide_schedule_changes(date)
    for detail in schedule_details:

        subscribers_services_detail = SubscriberServicesDetail(detail, Subscriber.objects.none(), detail.service_type)

        # Find anyone subscribed to any of the services for this schedule detail
        if detail.service_type == 'all':
            subscribers = Subscriber.objects.filter(status__exact='active')

            subscribers_services_detail.add(subscribers, ScheduleDetail.SERVICES_LIST)
        else:
            for service_type in detail.service_type.split(','):
                subscribers = Subscriber.objects.filter(status__exact='active')
                subscribers = subscribers.filter(service_type__contains='all') | subscribers.filter(service_type__contains=service_type)
                subscribers_services_detail.add(subscribers, service_type)

                # track which phone numbers we have texted citywide alerts
                content["citywide"].update( { subscriber.phone_number: 1 for subscriber in subscribers } )

        subscribers_services_details.append(subscribers_services_detail)

    # send text reminder to each subscriber needing a reminder
    for subscriber in subscribers_services.get_subscribers():

        message = get_service_message(subscribers_services.get_service(subscriber), date)
        MsgHandler().send_text(subscriber.phone_number, message, dry_run_param)

    # send out notifications about any schedule changes
    for subscribers_services_detail in subscribers_services_details:
        for subscriber in subscribers_services_detail.get_subscribers():

            message = get_service_detail_message(subscribers_services_detail.get_service(subscriber), subscribers_services_detail.schedule_detail)
            MsgHandler().send_text(subscriber.phone_number, message, dry_run_param)

    return Response(content)


@api_view(['GET'])
def get_route_info(request, format=None):
    """
    Output information about each waste collection route, grouped by day
    """

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
