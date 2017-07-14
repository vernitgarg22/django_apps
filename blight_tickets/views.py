from django.shortcuts import render

import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger

from blight_tickets.models import Tblztickets


@api_view(['GET'])
def get_ticket_list(request, year, month, day):
    """
    Returns list of all tickets for a given date.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # TODO put better query here...
    tickets = Tblztickets.objects.raw("select * from [COURT36TICKETS].[SWEETSpower].[tblZTickets] where zticketid = '22056'")
    ticket_list = [ ticket.zticketid for ticket in tickets ]
    content = { "tickets": ticket_list }

    return Response(content)
