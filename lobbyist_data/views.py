import json
import requests

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from .lobbyist import Lobbyist

import smartsheet


def get_cell_value(cells, idx):
    if len(cells) > idx + 1:
        cell = cells[idx]
        return cell.display_value or cell.value
    return None


@api_view(['GET'])
def lookup(request, format=None):
    """
    List lobbyist data
    """

    ACCESS_TOKEN = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_ACCESS_TOKEN']
    SHEETID = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_SHEETID']

    if request.method == 'GET':
        ssheet = smartsheet.Smartsheet(ACCESS_TOKEN)
        sheet = ssheet.Sheets.get_sheet(SHEETID)

        lobbyists = {}

        content = []
        for row in sheet.rows:
            regid = get_cell_value(row.cells, 0)
            name = get_cell_value(row.cells, 1)
            date = get_cell_value(row.cells, 2)
            
            if regid == None:
                continue

            lobbyist = lobbyists.get(regid)
            if lobbyist:
                lobbyist.add_date(date)
            else:
                lobbyist = Lobbyist(regid, name, date)
                lobbyists[regid] = lobbyist

        for lobbyist in sorted(lobbyists.values()):
            content.append(lobbyist.to_json())

        return Response(content)