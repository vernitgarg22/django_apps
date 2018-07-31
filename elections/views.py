import requests
import datetime
from datetime import date

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from elections.models import Poll, Precinct

import cod_utils.util
import cod_utils.security
from cod_utils.messaging import MsgHandler
from cod_utils.cod_logger import CODLogger


@api_view(['POST'])
def subscribe_notifications(request):
    """
    Parse subscription request and text user request for confirmation.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # # Only allow certain servers to call this endpoint
    # if cod_utils.security.block_client(request):
    #     remote_addr = request.META.get('REMOTE_ADDR')
    #     MsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
    #     return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    phone_number = request.data.get('phone_number')
    address = request.data.get('address')
    if not (phone_number and address):
        return Response({"error": "address and phone_number are required"}, status=status.HTTP_400_BAD_REQUEST)

    # text the subscriber to ask them to confirm
    MsgHandler().send_text(phone_number=phone_number, text="You will receive elections reminders for the address {}".format(address))

    return Response({ "received": { "phone_number": phone_number, "address": address }, "message": "New subscriber created" }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_polling_location(request, precinct):
    """
    Returns information about correct polling location for the precinct.
    """

    try:
        precinct = Precinct.objects.get(number=precinct)
    except ObjectDoesNotExist:
        raise Http404("Precinct number " + str(precinct) + " not found")

    return Response(precinct.poll.to_json())
