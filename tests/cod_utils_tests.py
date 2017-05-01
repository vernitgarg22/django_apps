import datetime

from django.test import Client
from django.test import TestCase, RequestFactory

import cod_utils.util
import cod_utils.security
import tests.disabled


class CODUtilsTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_date_json_date(self):
        str = cod_utils.util.date_json(datetime.date(2017, 5, 1))
        self.assertTrue(str == '2017-05-01T00:00:00', "date_json() converts date object to json")

    def test_date_json_datetime(self):
        str = cod_utils.util.date_json(datetime.datetime(2017, 5, 1, 00, 00, 00))
        self.assertTrue(str == '2017-05-01T00:00:00', "date_json() converts datetime object to json")

    def test_date_json_none(self):
        str = cod_utils.util.date_json(None)
        self.assertTrue(str == '', "date_json() converts null objects to empty string")

    def test_tomorrow(self):
        dt = cod_utils.util.tomorrow()
        self.assertTrue(datetime.date.today() - dt == datetime.timedelta(-1), "tomorrow() returns tomorrow")

    def test_tomorrow_string(self):
        dt = cod_utils.util.tomorrow("20170501")
        self.assertTrue(datetime.datetime.strptime("20170502", "%Y%m%d") == dt, "tomorrow() parses string and returns tomorrow")

    def test_block_client(self):
        # Force block_client to block us
        cod_utils.security.API_CLIENT_WHITELIST.remove("127.0.0.1")
        request = self.factory.request()
        blocked = cod_utils.security.block_client(request)
        self.assertTrue(blocked, "block_client() flags invalid callers")
        cod_utils.security.API_CLIENT_WHITELIST.append("127.0.0.1")

    def test_clean_list(self):
        values = [
            ([], []),
            ([''], []),
            (['a'], ['a']),
            (['a', ''], ['a']),
            (['a', ' '], ['a']),
            (['a', ' b'], ['a', 'b']),
            (['a', None], ['a', None]),
            (['a', 0], ['a', 0]),
            ]

        for input, expected in values:
            output = cod_utils.util.clean_list(input)
            self.assertEqual(expected, output, "clean_list() turns {} into {}".format(input, expected))

    def test_split_csv(self):
        values = [
            (None, []),
            ('', []),
            (',', []),
            (' ', []),
            ('a', ['a']),
            ('a,b', ['a', 'b']),
            ('a,,b', ['a', 'b']),
            (',a,,b', ['a', 'b']),
            ('a,,b,', ['a', 'b']),
            ]

        for input, expected in values:
            output = cod_utils.util.split_csv(input)
            self.assertEqual(expected, output, "split_csv() turns {} into {}".format(input, expected))

    def test_msg_handler(self):
        number = cod_utils.util.MsgHandler.get_phone_sender()
        self.assertTrue(type(number) is str and len(number) == 12, "get_phone_sender() returns a valid phone number")