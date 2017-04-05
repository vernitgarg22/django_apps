from datetime import datetime

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Subscriber
from waste_schedule.models import ScheduleDetail

from twilio.rest import TwilioRestClient
import twilio.twiml
# from twilio.util import RequestValidator


ACCOUNT_SID = "AC8b444a6aeeb1afdba3c064f2d105057d"
AUTH_TOKEN = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']
PHONE_SENDER = "+13132283402"


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

    # resp = twilio.twiml.Response()
    # resp.message("The Robots are coming! Head for the hills!")
    # return Response(resp)


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

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    # Find out which waste areas are about to get pickups
    routes = ScheduleDetail.find_waste_areas(date, ScheduleDetail.TRASH)
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
