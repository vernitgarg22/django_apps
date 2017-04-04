from datetime import datetime

from django.conf import settings
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Subscriber
from waste_schedule.models import ScheduleDetail

from twilio.rest import TwilioRestClient
import twilio.twiml


ACCOUNT_SID = "AC8b444a6aeeb1afdba3c064f2d105057d"
AUTH_TOKEN = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']
PHONE_SENDER = "+13132283402"


@api_view(['POST'])
def subscribe_notifications(request):
    """
    Parse subscription request and text user request for confirmation
    """

    data = request.data

    if not data.get('phone_number') or not data.get('waste_area_ids'):
        # TODO replace this with error 403 or something like that
        return Response({"error": "phone_number and waste_area_ids are required"})

    phone_number = data['phone_number']

    subscriber = Subscriber.objects.none()
    previous = Subscriber.objects.filter(phone_number__exact=phone_number)
    if previous.exists():
        subscriber = previous[0]
        subscriber.phone_number=phone_number
        subscriber.waste_area_ids=data['waste_area_ids']
        subscriber.status=Subscriber.DEFAULT_STATUS
    else:
        # try to create a subscriber with the posted data
        subscriber = Subscriber(phone_number=phone_number, waste_area_ids=data['waste_area_ids'])
    subscriber.save()

    # create a twilio client and text the subscriber to ask them to confirm
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        to = "+1" + subscriber.phone_number,
        from_ = PHONE_SENDER,
        body = "City of Detroit Public Works:  reply with YES to confirm that you want to receive trash & recycling pickup reminders",
    )

    # TODO return better response?
    return Response({ "received": str(subscriber) })

    # resp = twilio.twiml.Response()
    # with resp.message("Hello, Mobile Monkey") as m:
    #   m.media("https://demo.twilio.com/owl.png")
    # return str(resp)


@api_view(['POST'])
def confirm_notifications(request):
    """
    Parse subscription confirmation and send a simple response
    """
    return Response({ "confirmed": request.data })

    phone_number = request.data['phone_number']
    subscribers = Subscriber.objects.filter(phone_number__exact=phone_number)
    if not subscribers.exists():
        raise Http404("Subscriber not found")

    subscriber = subscribers[0]
    subscriber.activate()

    return Response({ "confirmed": str(subscriber) })



@api_view(['GET'])
def send_notifications(request, date=datetime.today(), format=None):
    """
    Send out any necessary notifications (e.g., regular schedule or schedule changes)
    """

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    # Find out which waste areas are about to get pickups
    routes = ScheduleDetail.find_waste_areas_extra(date, ScheduleDetail.TRASH)
    content = {}

    # get a list of route ids
    route_ids = [ int(id) for id in list(routes.keys()) if id ]
    for route_id in route_ids:

        # send text reminder to subscribers for this route
        subscribers = Subscriber.objects.using('default').filter(waste_area_ids__contains=str(route_id) + ',')
        content[route_id] = [ subscriber.phone_number for subscriber in subscribers ]

        for subscriber in subscribers:
            client.messages.create(
                to = "+1" + subscriber.phone_number,
                from_ = PHONE_SENDER,
                body = "Your next upcoming trash pickup is " + date.strftime("%b %d, %Y"),
            )

    return Response(content)
