from datetime import datetime, timedelta
import json
import requests

import mock
from unittest import skip
from unittest.mock import patch

from django.test import Client
from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from tests import test_util

from cod_utils import util

from waste_notifier.models import Subscriber


def cleanup_db():
    test_util.cleanup_model(Subscriber)


class WebsiteDataTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_get_amount_added(self):

        date = datetime.strptime('20180301', "%Y%m%d")
        date = timezone.make_aware(date)

        c = Client()
        response = c.get("/website_data/new_content/20180101/20180701/")

        expected = {
            "date_start": '2018-01-01T00:00:00',
            "date_end": '2018-07-01T00:00:00',
            "num_days": 181,
            "website_analytics": {
                "num_html_pages": 1190,
            },
            "waste_reminders": {
                "total_subscribers": 0,
                "new_subscribers": 0,
            }
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added should get returned")

    @mock.patch('django.utils.timezone.now')
    def test_get_amount_added_default(self, mocked_django_utils_timezone_now):

        date = datetime.strptime('20180814', "%Y%m%d")
        date = timezone.make_aware(date)

        mocked_django_utils_timezone_now.return_value = date

        c = Client()
        response = c.get("/website_data/new_content/")

        expected = {
            "date_start": '2018-08-13T00:00:00',
            "date_end": '2018-08-19T00:00:00',
            "num_days": 6,
            "website_analytics": {
                "num_html_pages": 886,
            },
            "waste_reminders": {
                "total_subscribers": 0,
                "new_subscribers": 0,
            }
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added should get returned")

    @mock.patch('django.utils.timezone.now')
    def test_get_amount_added_monday(self, mocked_django_utils_timezone_now):

        date = datetime.strptime('20180813', "%Y%m%d")
        date = timezone.make_aware(date)

        mocked_django_utils_timezone_now.return_value = date

        date = date - timedelta(days=7)

        c = Client()
        response = c.get("/website_data/new_content/")

        expected = {
            "date_start": '2018-08-06T00:00:00',
            "date_end": '2018-08-12T00:00:00',
            "num_days": 6,
            "website_analytics": {
                "num_html_pages": 899,
            },
            "waste_reminders": {
                "total_subscribers": 0,
                "new_subscribers": 0,
            }
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added should get returned")
