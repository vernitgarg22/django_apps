import requests
import datetime
from datetime import date
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from messenger.models import *
from messenger.util import get_messenger_msg_handler

from cod_utils import util
import cod_utils.security
from cod_utils.messaging import SlackMsgHandler, MsgHandler
from cod_utils.cod_logger import CODLogger


@api_view(['POST'])
def subscribe(request):
    """
    Parse subscription request and text user request for confirmation.

{
  'From': [
    '5005550007'
  ],
  'Body': [
    '7840 van dyke pl'
  ],
  'To': [
    '5005550006'
  ]
}

    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # # Only allow certain servers to call this endpoint
    # if cod_utils.security.block_client(request):
    #     remote_addr = request.META.get('REMOTE_ADDR')
    #     SlackMsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
    #     return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Verify required fields are present
    if not request.data.get('From') or not request.data.get('Body'):
        return Response({"error": "Address and phone_number are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Clean up phone numbers
    phone_number_from = MsgHandler.get_fone_number(request, key='From')
    phone_number_to = MsgHandler.get_fone_number(request, key='To')

    # Make sure phone number is set up and valid.
    if not MessengerPhoneNumber.objects.filter(phone_number=phone_number_to).exists():
        return Response({"error": "phone_number {phone_number_to} not found".format(phone_number_to=phone_number_to)},
            status=status.HTTP_404_NOT_FOUND)

    # Figure out what messenger client this is and get the msg handler for this client.
    phone_number_to_object = MessengerPhoneNumber.objects.get(phone_number=phone_number_to)
    client = phone_number_to_object.messenger_client

    msg_handler = get_messenger_msg_handler(client)

    # Make sure the call came from twilio and is valid
    # REVIEW: would be nice to validate earlier but we haven't yet been
    # able to construct our msg_handler until now...
    msg_handler.validate(request)

    # Clean up street address
    street_address = MsgHandler.get_address(request)

    # Parse address string and get result from AddressPoint geocoder
    location, address = util.geocode_address(street_address=street_address)
    if not location:
        invalid_addr_msg = 'Invalid {} signup: {} from {}'.format(client.name, street_address, phone_number_from)

        CODLogger.instance().log_error(name=__name__, area="Messenger signup by text", msg=invalid_addr_msg)

        SlackMsgHandler().send_admin_alert(invalid_addr_msg)

        msg = "Unfortunately, address {} could not be located - please text the street address only, for example '1301 3rd ave'".format(street_address)

        # REVIEW find a way to specify correct set of sender phone #s
        msg_handler.send_text(phone_number=phone_number_from, phone_sender=phone_number_to, text=msg)

        return Response({"error": "Street address '{}' not found".format(street_address)}, status=status.HTTP_400_BAD_REQUEST)

    # Create the Subscriber object
    subscriber = MessengerSubscriber(messenger_client=client, phone_number=phone_number_from, status='active',
        address=street_address, latitude=location['location']['y'], longitude=location['location']['x'])
    subscriber.save()

    # text the subscriber to ask them to confirm
    confirmation_message=client.confirmation_message.format(street_address=street_address, phone_number_from=phone_number_from)

    # REVIEW find a way to specify correct set of sender phone #s
    msg_handler.send_text(phone_number=phone_number_from, text=confirmation_message)

    response = { "received": { "phone_number": phone_number_from, "address": street_address }, "message": "New {} subscriber created".format(client.name) }
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_locations(request, format=None):
    """
    Returns all locations currently available.
    """

    return Response(get_locations_helper())


@api_view(['GET'])
def get_location_notifications(request, client_id, value, format=None):
    """
    Returns all notifications for the given client and location.
    """

    # REVIEW: Should really constrain location by location type

    client = get_existing_object(cl_type=MessengerClient, obj_id=client_id, cl_name="Client", required=True)

    if not MessengerLocation.objects.filter(value=value).exists():
        raise NotFound(detail={ "error": "Location {value} not found".format(value=value) })

    location = MessengerLocation.objects.filter(value=value).first()

    response = {
        "location": location.to_json(),
        "notifications": []
    }

    for notification in location.messengernotification_set.filter(messenger_client=client):

        response["notifications"].append(notification.to_json())

    return Response(response)


def get_existing_object(cl_type, obj_id, cl_name, required=False):
    """
    Returns existing object with id matching obj_id, if any.
    If obj_id is not None and the object cannot be found, a 404
    exception is thrown.
    if 'required' is True, then obj_id must not be None.
    """

    def raise_obj_error():
        raise NotFound(detail={ "error": "{cl_name} {obj_id} not found".format(cl_name=cl_name, obj_id=obj_id) })

    if not obj_id:
        if required:
            raise_obj_error()
        else:
            return None

    if type(obj_id) is str and not re.fullmatch(r'(\d)+', obj_id):
        raise_obj_error()

    obj_id = int(obj_id)
    if not cl_type.objects.filter(id=obj_id).exists():
        raise_obj_error()
    return cl_type.objects.get(id=obj_id)


@api_view(['POST'])
def add_notification(request, client_id, notification_id=None, format=None):
    """
    Creates or modifies a notification.

    {
        "day": "2019/11/05",
        "geo_layer_url": "https://arcgis.com/layer",
        "formatter": "ElectionsFormatter",
        "location_type": "ZIP Code",
        "locations": [ '48214', '48226' ]
    }
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    client = get_existing_object(cl_type=MessengerClient, obj_id=client_id, cl_name="Client", required=True)

    # Are we updating an existing notification?
    notification = get_existing_object(cl_type=MessengerNotification, obj_id=notification_id, cl_name="Notification")

    # Parse day.
    day_str = request.data.get("day", None)
    if not notification and not day_str:
        return Response({ "error": "Notification day is required" }, status=status.HTTP_400_BAD_REQUEST)

    if day_str:

        if not re.fullmatch(r'(\d){4}/(\d){2}/(\d){2}', day_str):
            return Response({ "error": "Notification day must use format YYYY/MM/DD" },
                status=status.HTTP_400_BAD_REQUEST)

        day = date(year=int(day_str[0:4]), month=int(day_str[5:7]), day=int(day_str[8:10]))

    else:

        day = notification.day

    # Parse geo layer url and formatter.
    geo_layer_url = request.data.get('geo_layer_url', None)
    formatter = request.data.get('formatter', None)

    # Create or update notification and save it.
    if not notification:
        notification = MessengerNotification(messenger_client=client, day=day, geo_layer_url=geo_layer_url, formatter=formatter)
    else:

        if day:
            notification.day = day
        if geo_layer_url:
            notification.geo_layer_url = geo_layer_url
        if formatter:
            notification.formatter = formatter

    notification.save()

    # Add our locations
    location_type = request.data.get("location_type")
    locations = request.data.getlist("locations")

    for value in locations:

        if not MessengerLocation.objects.filter(location_type=location_type, value=value).exists():
            return Response({ "error": "{location_type} with value {value} is invalid ".format(location_type=location_type, value=value) },
                status=status.HTTP_400_BAD_REQUEST)

        location = MessengerLocation.objects.get(location_type=location_type, value=value)
        if not notification.locations.filter(id=location.id).exists():
            notification.locations.add(location)

    return Response(notification.to_json(), status=status.HTTP_201_CREATED)

def get_notifications_helper(client_id, client_only=False):
    """
    Returns all notifications for a client.
    """

    client = get_existing_object(cl_type=MessengerClient, obj_id=client_id, cl_name="Client", required=True)

    if client_only:
        return client.to_json()

    response = {
        "client": client.to_json(),
        "notifications": []
    }

    for notification in client.messengernotification_set.all():

        response["notifications"].append(notification.to_json())

    return response


@api_view(['GET'])
def get_notifications(request, client_id=None):
    """
    Returns all notifications for a client.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    if client_id:

        return Response(get_notifications_helper(client_id=client_id))

    else:

        response = []

        for client in MessengerClient.objects.all():

            response.append(get_notifications_helper(client_id=client.id, client_only=True))

        return Response(response)


@api_view(['POST'])
def add_notification_message(request, notification_id, message_id=None):
    """
    Adds or updates a message for a notification.

    {
        "lang": "es",
        "message": "<insert message here>"
    }
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    notification = get_existing_object(cl_type=MessengerNotification, obj_id=notification_id, cl_name="Notification", required=True)

    messenger_message = get_existing_object(cl_type=MessengerMessage, obj_id=message_id, cl_name="Message")

    if not request.data.get('lang') or not request.data.get('message'):
        return Response({"error": "lang and message are required"}, status=status.HTTP_400_BAD_REQUEST)

    lang = request.data['lang']
    message = request.data['message']

    if not messenger_message:
        messenger_message = MessengerMessage(messenger_notification=notification, lang=lang, message=message)
    else:
        messenger_message.lang = lang
        messenger_message.message = message

    messenger_message.save()

    return Response(messenger_message.to_json(), status=status.HTTP_201_CREATED)
