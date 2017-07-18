from django.shortcuts import render

import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger

from blight_tickets.models import Tblztickets


# TODO remove this, if possible?
def clean_parcel_id(parcel_id):
    """
    Urls with dots are problematic: substitute underscores for dots in the url
    (and replace underscores with dots here)
    """
    return parcel_id.replace('_', '.')


@api_view(['GET'])
def get_ticket_info(request, parcel_id):
    """
    Returns list of all tickets for a given date.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_id = clean_parcel_id(parcel_id)

    tickets = Tblztickets.objects.raw("select * from [COURT36TICKETS].[SWEETSpower].[tblZTickets] where zticketid = {}".format(parcel_id))
    ticket_list = [ ticket.zticketid for ticket in tickets ]
    content = { "tickets": ticket_list }

    return Response(content)
