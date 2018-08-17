from datetime import datetime
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

from dnninternet.models import Faqs, Htmltext


def cleanup_db():
    test_util.cleanup_model(Faqs)
    test_util.cleanup_model(Htmltext)


class WebsiteDataTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_get_amount_added(self):

        date = datetime.strptime('20180301', "%Y%m%d")
        date = timezone.make_aware(date)

        faqs = Faqs(createdbyuser='karl', createddate=date, question='?', answer='A',
            categoryid=None, datemodified=date, viewcount=1, vieworder=1, faqhide=False,
            publishdate=date)
        faqs.save()

        htmltext = Htmltext(content='Dummy content', version=1, ispublished=True, 
            createdondate=date, lastmodifiedondate=date, publishdate=date)
        htmltext.save()

        c = Client()
        response = c.get("/website_data/new_content/20180101/20180701/")

        expected = {
            "num_faqs": 1,
            "num_html_pages": 1,
            "date_start": '2018-01-01T00:00:00',
            "date_end": '2018-07-01T00:00:00',
            "num_days": 181,
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added shoul get returned")

    def test_get_amount_added_default(self):

        date = datetime.strptime('20180813', "%Y%m%d")
        date = timezone.make_aware(date)

        faqs = Faqs(createdbyuser='karl', createddate=date, question='?', answer='A',
            categoryid=None, datemodified=date, viewcount=1, vieworder=1, faqhide=False,
            publishdate=date)
        faqs.save()

        htmltext = Htmltext(content='Dummy content', version=1, ispublished=True, 
            createdondate=date, lastmodifiedondate=date, publishdate=date)
        htmltext.save()

        c = Client()
        response = c.get("/website_data/new_content/")

        expected = {
            "num_faqs": 1,
            "num_html_pages": 1,
            "date_start": '2018-08-13T00:00:00',
            "date_end": '2018-08-19T00:00:00',
            "num_days": 6,
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added shoul get returned")

    @mock.patch('django.utils.timezone.now')
    def test_get_amount_added_monday(self, mocked_django_utils_timezone_now):

        date = datetime.strptime('20180813', "%Y%m%d")
        date = timezone.make_aware(date)

        # mocked_slackclient_api_call.return_value = {'ok': True}
        mocked_django_utils_timezone_now.return_value = date

        faqs = Faqs(createdbyuser='karl', createddate=date, question='?', answer='A',
            categoryid=None, datemodified=date, viewcount=1, vieworder=1, faqhide=False,
            publishdate=date)
        faqs.save()

        htmltext = Htmltext(content='Dummy content', version=1, ispublished=True, 
            createdondate=date, lastmodifiedondate=date, publishdate=date)
        htmltext.save()

        c = Client()
        response = c.get("/website_data/new_content/")

        expected = {
            "num_faqs": 1,
            "num_html_pages": 1,
            "date_start": '2018-08-13T00:00:00',
            "date_end": '2018-08-19T00:00:00',
            "num_days": 6,
        }

        self.assertEqual(response.status_code,  200)
        self.assertEqual(expected, response.data, "Summary of data added shoul get returned")
