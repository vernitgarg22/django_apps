import datetime

from django.test import Client
from django.test import TestCase, RequestFactory

from cod_utils import util
from cod_utils import security
import tests.disabled


class CODUtilsTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_date_json_date(self):
        str = util.date_json(datetime.date(2017, 5, 1))
        self.assertTrue(str == '2017-05-01T00:00:00', "date_json() converts date object to json")

    def test_date_json_datetime(self):
        str = util.date_json(datetime.datetime(2017, 5, 1, 00, 00, 00))
        self.assertTrue(str == '2017-05-01T00:00:00', "date_json() converts datetime object to json")

    def test_date_json_none(self):
        str = util.date_json(None)
        self.assertTrue(str == '', "date_json() converts null objects to empty string")

    def test_tomorrow(self):
        dt = util.tomorrow()
        self.assertTrue(datetime.date.today() - dt == datetime.timedelta(-1), "tomorrow() returns tomorrow")

    def test_tomorrow_string(self):
        dt = util.tomorrow("20170501")
        self.assertTrue(datetime.datetime.strptime("20170502", "%Y%m%d") == dt, "tomorrow() parses string and returns tomorrow")

    def test_get_week_start_end_fri(self):
        start, end = util.get_week_start_end(datetime.date(2017, 5, 5))
        self.assertEqual(start, datetime.date(2017, 5, 1))
        self.assertEqual(end, datetime.date(2017, 5, 7))

    def test_get_week_start_end_mon(self):
        start, end = util.get_week_start_end(datetime.date(2017, 5, 1))
        self.assertEqual(start, datetime.date(2017, 5, 1))
        self.assertEqual(end, datetime.date(2017, 5, 7))

    def test_get_week_start_end_sun(self):

        start, end = util.get_week_start_end(datetime.date(2017, 5, 1))
        self.assertEqual(start, datetime.date(2017, 5, 1))
        self.assertEqual(end, datetime.date(2017, 5, 7))

    def test_block_client(self):
        # Force block_client to block us
        security.API_CLIENT_WHITELIST.remove("127.0.0.1")
        request = self.factory.request()
        blocked = security.block_client(request)
        self.assertTrue(blocked, "block_client() flags invalid callers")
        security.API_CLIENT_WHITELIST.append("127.0.0.1")

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
            output = util.clean_list(input)
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
            output = util.split_csv(input)
            self.assertEqual(expected, output, "split_csv() turns {} into {}".format(input, expected))


class CODUtilsMsgHandlerTests(TestCase):

    def setUp(self):
        self.dry_run_previous = util.MsgHandler.DRY_RUN

    def tearDown(self):
        util.MsgHandler.DRY_RUN = self.dry_run_previous

    def test_get_phone_sender(self):
        number = util.MsgHandler.get_phone_sender()
        self.assertTrue(type(number) is str and len(number) == 12, "get_phone_sender() returns a valid phone number")

    def test_send_message(self):
        util.MsgHandler.DRY_RUN = False
        sent = util.MsgHandler().send_text("5005550006", "testing")
        self.assertTrue(sent, "MsgHandler sends a text")

    def test_send_message_dry_run(self):
        util.MsgHandler.DRY_RUN = True
        sent = util.MsgHandler().send_text("5005550006", "testing")
        self.assertFalse(sent, "MsgHandler sends no texts when DRY_RUN is set")

    def test_send_message_dry_run_param(self):
        util.MsgHandler.DRY_RUN = False
        sent = util.MsgHandler().send_text("5005550006", "testing", dry_run_param = True)
        self.assertFalse(sent, "MsgHandler sends no texts when dry_run_param is True")
