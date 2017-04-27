import datetime

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

import cod_utils.util
import tests.disabled

from waste_schedule.models import ScheduleDetail

import waste_schedule.views


# TODO put this in a util.py file
def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(ScheduleDetail)


class WasteScheduleTests(TestCase):

    def util_test_get_next_pickups(self, today, route_ids, expected):
        """
        Utility function to run test pickups
        """
        cleanup_db()
        c = Client()
        response = c.get("/waste_schedule/details/{0}/?today={1}".format(route_ids, today))

        self.assertTrue(response.status_code == 200)
        self.assertDictEqual(expected, response.data, "Routes {} should get it's pickups predicted correctly".format(route_ids))

    def test_get_next_oneday_pickups(self):
        """
        Test getting next pickups for routes that have all pickups on the same day (e.g., route 8)
        """

        self.maxDiff = None

        values = {
            0: {'next_pickups': {'recycling': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'trash': {'route': 0, 'next_pickup': '2017-05-01T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'bulk': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}}, 'details': []},
            8: {'next_pickups': {'recycling': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'trash': {'route': 8, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'bulk': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}}, 'details': []},
            9: {'next_pickups': {'recycling': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'trash': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'bulk': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}}, 'details': []},
        }

        today = "20170427"

        for route_id in values.keys():
            self.util_test_get_next_pickups(today, route_id, values[route_id])

    def test_get_next_multiday_pickups(self):
        """
        Test getting next pickups for routes that have all pickups on different days (e.g., route 8)
        """

        self.maxDiff = None

        values = {
            '11,28,35': {'next_pickups': {'bulk': {'next_pickup': '2017-05-04T00:00:00', 'week': 'a', 'day': 'thursday', 'contractor': 'advance', 'route': 35}, 'trash': {'next_pickup': '2017-05-03T00:00:00', 'week': ' ', 'day': 'wednesday', 'contractor': 'advance', 'route': 11}, 'recycle': {'next_pickup': '2017-04-27T00:00:00', 'week': 'b', 'day': 'thursday', 'contractor': 'advance', 'route': 28}}, 'details': []},
            '14,27,31': {'next_pickups': {'recycle': {'week': 'a', 'day': 'monday', 'contractor': 'advance', 'route': 27, 'next_pickup': '2017-05-01T00:00:00'}, 'bulk': {'week': 'a', 'day': 'tuesday', 'contractor': 'advance', 'route': 31, 'next_pickup': '2017-05-02T00:00:00'}, 'trash': {'week': ' ', 'day': 'monday', 'contractor': 'advance', 'route': 14, 'next_pickup': '2017-05-01T00:00:00'}}, 'details': []},
        }

        today = "20170427"

        for route_ids in values.keys():
            self.util_test_get_next_pickups(today, route_ids, values[route_ids])
