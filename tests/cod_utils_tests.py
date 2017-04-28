import datetime

from django.test import Client
from django.test import TestCase

import cod_utils.util
import tests.disabled


class CODUtilsTests(TestCase):

    def test_date_json_date(self):
        str = cod_utils.util.date_json(datetime.date(2017, 5, 1))
        self.assertTrue(str == '2017-05-01T00:00:00', "date_json() converts date object to json")

    def test_date_json_datetime(self):
        str = cod_utils.util.date_json(datetime.datetime(2017, 5, 1, 00, 00, 00))
        self.assertTrue(str == '2017-05-01T00:00:00', "date_json() converts datetime object to json")

    def test_tomorrow(self):
        dt = cod_utils.util.tomorrow()
        self.assertTrue(datetime.date.today() - dt == datetime.timedelta(-1), "tomorrow() returns tomorrow")

    def test_tomorrow_string(self):
        dt = cod_utils.util.tomorrow("20170501")
        self.assertTrue(datetime.datetime.strptime("20170502", "%Y%m%d") == dt, "tomorrow() parses string and returns tomorrow")

    def test_msg_handler(self):
        number = cod_utils.util.MsgHandler.get_phone_sender()
        self.assertTrue(type(number) is str and len(number) == 12, "get_phone_sender() returns a valid phone number")