import json
import requests

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.http import Http404
from .attachment import Attachment
from .client import Client
from .lobbyist import Lobbyist
from .lobbyist_data import LobbyistData

from rest_framework.parsers import JSONParser


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
    LOBBYIST_DATA_SHEETID = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_SHEETID']
    LOBBYIST_CLIENT_SHEET_ID = settings.AUTO_LOADED_DATA['LOBBYIST_CLIENT_SHEET_ID']

    if request.method == 'GET':
        ssheet = smartsheet.Smartsheet(ACCESS_TOKEN)
        sheet = ssheet.Sheets.get_sheet(LOBBYIST_DATA_SHEETID)

        lobbyists = LobbyistData()

        for row in sheet.rows:
            regid = get_cell_value(row.cells, 0)
            name = get_cell_value(row.cells, 1)
            date = get_cell_value(row.cells, 2)

            attachment = None

            rowTmp = ssheet.Sheets.get_row(LOBBYIST_DATA_SHEETID, row.id, include='attachments')
            if len(rowTmp.attachments):
                attachment = Attachment(rowTmp.attachments[0].id, rowTmp.attachments[0].name)

            if regid != None:
                lobbyists.add_lobbyist(regid, name, date, attachment)

        sheet = ssheet.Sheets.get_sheet(LOBBYIST_CLIENT_SHEET_ID)
        for row in sheet.rows:
            regid = get_cell_value(row.cells, 0)
            name = get_cell_value(row.cells, 1)
            address = get_cell_value(row.cells, 2)
            city = get_cell_value(row.cells, 3)
            state = get_cell_value(row.cells, 4)
            zipcode = get_cell_value(row.cells, 5)
            phone = get_cell_value(row.cells, 6)
            start_date = get_cell_value(row.cells, 7)
            # end_date = get_cell_value(row.cells, 8)

            client = Client(name, address, city, state, zipcode, phone, start_date)
            lobbyists.add_client(regid, client)

        return Response(lobbyists.to_json())


@api_view(['GET'])
def file(request, format=None):
    """
    Return lobbyist filing
    """

    ACCESS_TOKEN = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_ACCESS_TOKEN']
    LOBBYIST_DATA_SHEETID = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_SHEETID']

    if request.method == 'GET':
        ssheet = smartsheet.Smartsheet(ACCESS_TOKEN)

        # TODO get this from kwargs
        # attachmentId = 6945649062111108
        attachmentId = request.path_info.split('/')[4]
        attachment = ssheet.Attachments.get_attachment(LOBBYIST_DATA_SHEETID, attachmentId)

        if type(attachment) is not smartsheet.models.attachment.Attachment:
             raise Http404("Attachment does not exist")

        content = {
            "id": attachment.id,
            "name": attachment.name,
            "mimeType": attachment.mime_type,
            "url": attachment.url
        }

        return Response(content)
