from datetime import date
from datetime import datetime
from datetime import timedelta
import pytz

from cod_utils.messaging import SlackMsgHandler

from django.conf import settings

from django.test import Client
from django.test import TestCase, RequestFactory
from unittest import skip
import mock
from unittest.mock import patch

from cod_utils import util
from cod_utils import security
from cod_utils.messaging import MsgHandler, get_dpw_msg_handler

from slackclient import SlackClient


class CODUtilsTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_date_json_date(self):
        str = util.date_json(date(2017, 5, 1))
        self.assertTrue(str == '2017-05-01T00:00:00.000Z', "date_json() converts date object to json")

    def test_date_json_datetime(self):
        str = util.date_json(datetime(2017, 5, 1, 00, 00, 00))
        self.assertTrue(str == '2017-05-01T00:00:00.000Z', "date_json() converts datetime object to json")

    def test_date_json_none(self):
        str = util.date_json(None)
        self.assertTrue(str == '', "date_json() converts null objects to empty string")

    def test_get_local_time(self):
        utc = datetime(2001, 1, 1, 12, 1, tzinfo=pytz.utc)
        local = util.get_local_time(utc)
        self.assertEqual(utc, local, "get_localtime() converts datetime value to local")
        self.assertTrue(utc.hour - local.hour == 5) # this might break during DST

    def test_tomorrow(self):
        dt = util.tomorrow()
        self.assertTrue(date.today() - dt == timedelta(-1), "tomorrow() returns tomorrow")

    def test_tomorrow_string(self):
        dt = util.tomorrow("20170501")
        self.assertTrue(datetime.strptime("20170502", "%Y%m%d") == dt, "tomorrow() parses string and returns tomorrow")

    def test_get_week_start_end_fri(self):
        start, end = util.get_week_start_end(date(2017, 5, 5))
        self.assertEqual(start, date(2017, 5, 1))
        self.assertEqual(end, date(2017, 5, 7))

    def test_get_week_start_end_mon(self):
        start, end = util.get_week_start_end(date(2017, 5, 1))
        self.assertEqual(start, date(2017, 5, 1))
        self.assertEqual(end, date(2017, 5, 7))

    def test_get_week_start_end_sun(self):

        start, end = util.get_week_start_end(date(2017, 5, 1))
        self.assertEqual(start, date(2017, 5, 1))
        self.assertEqual(end, date(2017, 5, 7))

    @skip('Blocking clients by IP not permitted by firewall')
    def test_block_client(self):
        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")
        request = self.factory.request()
        blocked = security.block_client(request)
        self.assertTrue(blocked, "block_client() flags invalid callers")
        settings.ALLOWED_HOSTS.append("127.0.0.1")

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
        self.dry_run_previous = MsgHandler.DRY_RUN

    def tearDown(self):
        MsgHandler.DRY_RUN = self.dry_run_previous

    def test_get_phone_sender(self):
        number = get_dpw_msg_handler().get_phone_sender()
        self.assertTrue(type(number) is str and len(number) == 12, "get_phone_sender() returns a valid phone number")

    def test_get_phone_sender_consistent(self):

        msg_handler = get_dpw_msg_handler()

        numbers = [
            '1234567800', '1234567801', '1234567802', '1234567803', '1234567804', '1234567805', '1234567806', '1234567807', '1234567808', '1234567809',
            '1234567810', '1234567811', '1234567812', '1234567813', '1234567814', '1234567815', '1234567816', '1234567817', '1234567818', '1234567819',
            ]

        for number in numbers:
            key = MsgHandler.get_phone_number_key(number)
            msg_handler.phone_senders[key] = number

        for number in numbers:
            sender = msg_handler.get_phone_sender(dest_phone_number=number)
            self.assertEqual(sender, number, "MsgHandler uses consistent fone numbers")

    def test_send_message(self):
        MsgHandler.DRY_RUN = False
        sent = get_dpw_msg_handler().send_text("5005550006", "testing")
        self.assertTrue(sent, "MsgHandler sends a text")

    def test_send_message_dry_run(self):
        MsgHandler.DRY_RUN = True
        sent = get_dpw_msg_handler().send_text("5005550006", "testing")
        self.assertFalse(sent, "MsgHandler sends no texts when DRY_RUN is set")

    def test_send_message_dry_run_param(self):
        MsgHandler.DRY_RUN = False
        sent = get_dpw_msg_handler().send_text("5005550006", "testing", dry_run_param = True)
        self.assertFalse(sent, "MsgHandler sends no texts when dry_run_param is True")

    @mock.patch('slackclient.SlackClient.api_call')
    def test_send_admin_alert(self, mocked_slackclient_api_call):

        mocked_slackclient_api_call.return_value = {'ok': True}
        previous_dry_run = SlackMsgHandler.DRY_RUN
        MsgHandler.DRY_RUN = False
        sent = SlackMsgHandler().send_admin_alert(message="testing")
        self.assertTrue(sent, "MsgHandler sends an admin alert")
        MsgHandler.DRY_RUN = previous_dry_run


class SlackMsgHandlerTests(TestCase):

    def setUp(self):
        self.dry_run_previous = MsgHandler.DRY_RUN

    def tearDown(self):
        MsgHandler.DRY_RUN = self.dry_run_previous

    def test_slack_thread_dryrun(self):

        SlackMsgHandler.DRY_RUN = True
        slack_msg_handler = SlackMsgHandler()

        self.assertFalse(slack_msg_handler.send(message='testing plz ignore - start thread'))
        self.assertFalse(slack_msg_handler.comment(message='testing plz ignore - continue thread'))
        self.assertFalse(slack_msg_handler.comment(message='testing plz ignore - finish thread'))

    def test_slack_thread(self):

        MockedReturnValue = {
            'ok': True,
            'ts': 1,
        }

        SlackMsgHandler.DRY_RUN = False
        slack_msg_handler = SlackMsgHandler()

        with patch.object(SlackClient, 'api_call') as mock_method:

            mock_method.return_value = MockedReturnValue

            self.assertTrue(slack_msg_handler.send(message='testing plz ignore - start thread'))
            self.assertTrue(slack_msg_handler.comment(message='testing plz ignore - continue thread'))
            self.assertTrue(slack_msg_handler.comment(message='testing plz ignore - finish thread'))
