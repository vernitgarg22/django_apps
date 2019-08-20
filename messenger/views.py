import requests
import datetime
from datetime import date

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerSubscriber
from messenger.util import get_messenger_msg_handler

from cod_utils import util
import cod_utils.security
from cod_utils.messaging import SlackMsgHandler, MsgHandler
from cod_utils.cod_logger import CODLogger


@api_view(['POST'])
def subscribe(request):
    """
    Parse subscription request and text user request for confirmation.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # # Only allow certain servers to call this endpoint
    # if cod_utils.security.block_client(request):
    #     remote_addr = request.META.get('REMOTE_ADDR')
    #     SlackMsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
    #     return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)


    # Make sure the call came from twilio and is valid
    MsgHandler.validate(request)

    # Verify required fields are present
    if not request.data.get('From') or not request.data.get('Body'):
        return Response({"error": "Address and phone_number are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Clean up phone numbers
    phone_number_from = MsgHandler.get_fone_number(request, key='From')
    phone_number_to = MsgHandler.get_fone_number(request, key='To')

    # Make sure phone number is set up and valid.
    if not MessengerPhoneNumber.objects.filter(phone_number=phone_number_to).exists():
        return Response({"error": f"phone_number {phone_number_to} not found"}, status=status.HTTP_404_NOT_FOUND)

    # Figure out what messenger client this is and get the msg handler for this client.
    phone_number_to_object = MessengerPhoneNumber.objects.get(phone_number=phone_number_to)
    client = phone_number_to_object.messenger_client

    msg_handler = get_messenger_msg_handler(client)

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
