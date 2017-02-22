import json
import requests

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings

import smartsheet


def index(request):
    return HttpResponse("Hello, world. You're at the lookup index.")

def get_cell_value(cells, idx):
    if len(cells) > idx + 1:
        return cells[idx].display_value
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

        last_name = ""

        content = []
        for row in sheet.rows:
            name = get_cell_value(row.cells, 0)
            value = get_cell_value(row.cells, 1)
            last_name = name or last_name
            content.append( { last_name: value } )

        return Response(content)