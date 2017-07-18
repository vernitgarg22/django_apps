from django.shortcuts import render

import requests

from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger

from blight_tickets.models import Tblztickets


@api_view(['GET'])
def get_ticket_info(request, ticket_id):
    """
    Returns list of all tickets for a given date.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    table_name = "[COURT36TICKETS].[SWEETSpower].[tblZTickets]"
    if settings.RUNNING_UNITTESTS:
        table_name = "tblZTickets"

    tickets = Tblztickets.objects.raw("select * from {} where zticketid = {}".format(table_name, ticket_id))
    ticket_list = [ ticket.zticketid for ticket in tickets ]
    content = { "tickets": ticket_list }

    return Response(content)
