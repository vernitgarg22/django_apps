from datetime import datetime

import mock
from unittest.mock import patch

from django.test import Client, TestCase
from django.utils import timezone
import django.utils

from car_info.models import LicensePlateInfo

from cod_utils.util import date_json

from tests import test_util


class CarInfoTests(TestCase):

    def cleanup_db(self):
        test_util.cleanup_model(LicensePlateInfo)

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test.
        """
        self.cleanup_db()
        self.maxDiff = None

    # Test adding license plate info.
    def test_add_info(self):

        time_right_now = datetime.now(timezone.utc)

        with patch.object(timezone, 'localtime', return_value=time_right_now) as mock_now:

            c = Client()

            response = c.post('/car_info/', { "plate_num": "dummy12" } )

            expected = { "message": "Plate number added", "date_added": date_json(time_right_now) }
            self.assertEqual(response.status_code, 201)
            self.assertDictEqual(response.data, expected, "License plate number can be added")

    # Test adding the same license plate info twice.
    def test_add_info_twice(self):

        plate_info = LicensePlateInfo(plate_num='dummy12')
        plate_info.save()

        c = Client()

        response = c.post('/car_info/', { "plate_num": "dummy12" } )

        expected = { "message": "Error: plate number already added", "date_added": date_json(plate_info.created_at) }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, expected, "A license plate number can be added only once")

    # Test adding the different license plate info.
    def test_add_unique_info(self):

        c = Client()

        response = c.post('/car_info/', { "plate_num": "dummy12" } )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Plate number added", "A new license plate number can be added")

        response = c.post('/car_info/', { "plate_num": "dummy13" } )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Plate number added", "Another license plate number can be added")

    # Test adding license plate info.
    def test_add_info_missing_plate_num(self):

        c = Client()

        response = c.post('/car_info/', {})
        self.assertEqual(response.status_code, 400)
