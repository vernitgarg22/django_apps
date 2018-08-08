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
from elections.models import Precinct, Poll


class ElectionsTests(TestCase):

    def cleanup_db(self):
        pass

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        self.cleanup_db()
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
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")


class ElectionPollingInfoTests(TestCase):

    def cleanup_db(self):
        for model in [ Precinct, Poll ]:
            test_util.cleanup_model(model)

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        self.cleanup_db()
        self.maxDiff = None

    def test_get_polling_location(self):

        poll = Poll(name='test', address='800 woodward detroit, mi',
            latitude=42.0, longitude=82.1,
            congress_rep_district=1, state_senate_district=1, state_rep_district=1,
            map_url="https://goo.gl/maps/xfFuRHgY2dC2", image_url="https://goo.gl/maps/4ijaK7hjUKr")
        poll.save()
        precinct = Precinct(poll=poll, number=1)
        precinct.save()

        c = Client()

        response = c.get('/elections/poll/1/', Secure=True)

        expected = {
            'name': 'test',
            'address': '800 woodward detroit, mi',
            'latitude': 42.0,
            'longitude': 82.1,
            'congress_rep_district': 1,
            'state_senate_district': 1,
            'state_rep_district': 1,
            'map': 'https://goo.gl/maps/xfFuRHgY2dC2',
            'image': 'https://goo.gl/maps/4ijaK7hjUKr',
            'precincts': [1]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_get_polling_location_not_found(self):

        c = Client()

        response = c.get('/elections/poll/1/', Secure=True)
        self.assertEqual(response.status_code, 404)

