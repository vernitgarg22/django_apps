import json
import requests

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.http import Http404
from .attachment import Attachment
from .registration import Registration
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


def add_lobbyists(ssheet, sheet_id, lobbyists):
    """
    Populate lobbyst data, including lobbyst registration attachment data
    """
    sheet = ssheet.Sheets.get_sheet(sheet_id)
    for row in sheet.rows:
        regid = get_cell_value(row.cells, 0)
        name = get_cell_value(row.cells, 1)
        date = get_cell_value(row.cells, 2)
        address = get_cell_value(row.cells, 3)
        city = get_cell_value(row.cells, 4)
        state = get_cell_value(row.cells, 5)
        zipcode = get_cell_value(row.cells, 6)
        phone = get_cell_value(row.cells, 7)
        reg_type_fed = get_cell_value(row.cells, 8)
        reg_type_mi = get_cell_value(row.cells, 9)
        reg_type_state_other = get_cell_value(row.cells, 10)
        expend_1000 = get_cell_value(row.cells, 11)
        expend_250 = get_cell_value(row.cells, 12)

        attachment = None

        rowTmp = ssheet.Sheets.get_row(sheet_id, row.id, include='attachments')
        if len(rowTmp.attachments):
            attachment = Attachment(rowTmp.attachments[0].id, rowTmp.attachments[0].name)

        if regid != None:
            lobbyist = lobbyists.add_lobbyist(regid, name)
            registration = Registration(date, address, city, state, zipcode, phone, reg_type_fed, reg_type_mi, reg_type_state_other, expend_1000, expend_250, attachment)
            lobbyist.add_registration(registration)


def add_clients(ssheet, sheet_id, lobbyists):
    """
    Populate lobbyist client data
    """
    sheet = ssheet.Sheets.get_sheet(sheet_id)
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


@api_view(['GET'])
def lookup(request, format=None):
    """
    List lobbyist data
    """

    ACCESS_TOKEN = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_ACCESS_TOKEN']
    LOBBYIST_DATA_SHEET_ID = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_SHEET_ID']
    LOBBYIST_CLIENT_SHEET_ID = settings.AUTO_LOADED_DATA['LOBBYIST_CLIENT_SHEET_ID']

    if request.method == 'GET':
        ssheet = smartsheet.Smartsheet(ACCESS_TOKEN)

        lobbyists = LobbyistData()

        add_lobbyists(ssheet, LOBBYIST_DATA_SHEET_ID, lobbyists)
        add_clients(ssheet, LOBBYIST_CLIENT_SHEET_ID, lobbyists)

        return Response(lobbyists.to_json())


@api_view(['GET'])
def file(request, format=None):
    """
    Return lobbyist filing
    """

    ACCESS_TOKEN = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_ACCESS_TOKEN']
    LOBBYIST_DATA_SHEET_ID = settings.AUTO_LOADED_DATA['LOBBYIST_DATA_SHEET_ID']

    if request.method == 'GET':
        ssheet = smartsheet.Smartsheet(ACCESS_TOKEN)

        # TODO get this from kwargs
        # attachmentId = 6945649062111108
        attachmentId = request.path_info.split('/')[4]
        attachment = ssheet.Attachments.get_attachment(LOBBYIST_DATA_SHEET_ID, attachmentId)

        if type(attachment) is not smartsheet.models.attachment.Attachment:
             raise Http404("Attachment does not exist")

        content = {
            "id": attachment.id,
            "name": attachment.name,
            "mimeType": attachment.mime_type,
            "url": attachment.url
        }

        return Response(content)
