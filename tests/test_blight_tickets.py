from datetime import datetime, tzinfo
import json

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.utils import timezone

from django.test import Client
from django.test import TestCase

import tests.disabled

from blight_tickets.models import Tblztickets

import photo_survey.views


def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(Tblztickets)

def create_ticket():

    dt_val = timezone.now()

    ticket = Tblztickets(zticketid=1, ticketnumber='05006271DAH', agencyid=3, violstreetnumber=2900, violstreetname=1802, violzipcode=None, violdescid=641, issuedate=dt_val, issuetime=dt_val, courttime=2, initialcourttime=2, courtdate=dt_val, canceledby=0, canceldate=None, cancelreason=None, voidticket=0, origfineamt=2033, newfineamt=0, adjjudgmentamt=None, jsa=10, adminfee=20, latefee=0, discamt=0, remediationcost=0, serve=1, cityoffsign=539, courtcnsl=0, courtcnsldt=None, zticketuserid=539, zticketupdatedt=dt_val, chptrid=3, repeatoffenderflag=0, inspectornote=None, attorneyid=None, tickettype='DAH', crtrmid=1, clearused=None, clearnum=None, clearrecordid=None, modifiedby=None, modifieddt=None, stay=None, ticketprintflag=None, ticketprintdt=None)
    ticket.save()
    return ticket


class BlightTicketsTests(TestCase):

    def setUp(self):
        cleanup_db()

    def test_get_ticket_info(self):

        ticket = create_ticket()

        c = Client()

        response = c.get("/blight_tickets/ticket_info/{}/".format(ticket.zticketid))
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'tickets': [1]}, response.data, "/blight_tickets/ticket_info/<zticketid>/ returns ticket info")
