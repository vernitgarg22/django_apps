import datetime

from django.conf import settings

from django.test import Client, TestCase

from django.core.exceptions import ValidationError

import mock
from unittest import skip
from unittest.mock import patch

import cod_utils.util
import cod_utils.security
from cod_utils.messaging import MsgHandler
from cod_utils.util import date_json

from slackclient import SlackClient

import tests.disabled
from tests import test_util

from elections import views


def cleanup_db():
    pass


class ElectionsTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()
        self.maxDiff = None

    # Test actual API endpoints
    def test_subscribe_msg(self):

        c = Client()

        response = c.post('/elections/subscribe/', { "phone_number": "5005550006", "address": "1104 Military St" } )

        expected = {'received': {'phone_number': '5005550006', 'address': '1104 Military St'}, 'message': 'New subscriber created'}
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_fone(self):

        c = Client()

        response = c.post('/elections/subscribe/', { "address": "1104 Military St" } )

        expected = {'error': 'address and phone_number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_address(self):

        c = Client()

        response = c.post('/elections/subscribe/', { "phone_number": "5005550006" } )

        expected = {'error': 'address and phone_number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")
