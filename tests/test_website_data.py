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


def check_node_count(result):

    if not result or len(result[0].values()) != 1 or not result[0].values()[0]:
        raise Exception('Invalid result value encountered')
    return 100


class WebsiteDataTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    @mock.patch('website_data.views.get_node_count')
    def test_get_amount_added(self, mocked_get_node_count):

        mocked_get_node_count.side_effect = check_node_count

        date = datetime.strptime('20180301', "%Y%m%d")
        date = timezone.make_aware(date)

        c = Client()
        response = c.get("/website_data/new_content/20180101/20180701/")

        expected = {
            "date_start": '2018-01-01T00:00:00',
            "date_end": '2018-07-01T00:00:00',
            "num_days": 181,
            "website_analytics": {
                "num_new_html_pages": 200,
                "num_total_html_pages": 200,
            },
            "waste_reminders": {
                "total_subscribers": 0,
                "new_subscribers": 0,
            }
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added should get returned")

    @mock.patch('django.utils.timezone.now')
    @mock.patch('website_data.views.get_node_count')
    def test_get_amount_added_default(self, mocked_get_node_count, mocked_django_utils_timezone_now):

        mocked_get_node_count.side_effect = check_node_count

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
                "num_new_html_pages": 200,
                "num_total_html_pages": 200,
            },
            "waste_reminders": {
                "total_subscribers": 0,
                "new_subscribers": 0,
            }
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added should get returned")

    @mock.patch('django.utils.timezone.now')
    @mock.patch('website_data.views.get_node_count')
    def test_get_amount_added_monday(self, mocked_get_node_count, mocked_django_utils_timezone_now):

        mocked_get_node_count.side_effect = check_node_count

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
                "num_new_html_pages": 200,
                "num_total_html_pages": 200,
            },
            "waste_reminders": {
                "total_subscribers": 0,
                "new_subscribers": 0,
            }
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added should get returned")
