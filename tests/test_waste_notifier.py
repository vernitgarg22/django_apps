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

from waste_notifier.models import Subscriber
from waste_notifier.util import *
from waste_schedule.models import ScheduleDetail, BiWeekType
from waste_schedule.schedule_detail_mgr import ScheduleDetailMgr

from waste_notifier import views
from waste_notifier import util


def cleanup_db():
    test_util.cleanup_model(Subscriber)
    test_util.cleanup_model(ScheduleDetail)


def add_meta(content, date = cod_utils.util.tomorrow()):
    """
    Add meta data for the /send endpoint (e.g., date)
    """

    week_type = ScheduleDetail.get_date_week_type(date)
    meta = {
        'meta': {
            'current_time': datetime.datetime.today().strftime("%Y-%m-%d %H:%M"),
            'date_applicable': date.strftime("%Y-%m-%d"),
            "week_type": str(week_type),
            'dry_run': True
        }
    }
    content.update(meta)
    return content

def make_subscriber(waste_area_ids=None, service_type="all", address="7840 Van Dyke Pl", phone_number="5005550006"):

    if not waste_area_ids:

        location, _ = geocode_address(street_address=address)
        waste_area_ids = get_waste_area_ids(location=location)
        waste_area_ids = ''.join( [ str(num) + ',' for num in waste_area_ids ] )

    subscriber = Subscriber(phone_number=phone_number, waste_area_ids=waste_area_ids, address=address, service_type=service_type)
    subscriber.activate()
    return subscriber


class WasteNotifierTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()
        self.maxDiff = None

    def test_subscriber_comment(self):
        """
        Test subscriber with comment
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", address="7840 van dyke pl", service_type="all")
        s.save()
        views.add_subscriber_comment(subscriber=s, comment="testing")
        s = Subscriber.objects.first()
        self.assertTrue(str(s).find("testing"), "add_subscriber_comment() adds a comment to the subscriber")

    def test_subscriber_comment_truncate(self):
        """
        Test subscriber with long comment getting truncated.
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", address="7840 van dyke pl", service_type="all")
        s.save()
        views.add_subscriber_comment(subscriber=s, comment = "testing" * 1000)
        s = Subscriber.objects.first()
        self.assertTrue(str(s).find("(previous comments truncated)"), "add_subscriber_comment() truncates a comment to the subscriber")

    def test_subscriber_delete(self):
        """
        Verify that deleting a subscriber does a 'soft delete'
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", address="7840 van dyke pl", service_type="all")
        s.delete()
        self.assertEqual(s.status, 'inactive', "Deleting a subscriber causes a 'soft delete'")

    def test_update_or_create_from_dict(self):
        """
        Test creating a subscriber from a dict object
        """
        s, error = Subscriber.update_or_create_from_dict( { "phone_number": "1234567890", "address": "1104 Military St", "service_type": "all" } )
        self.assertEqual(error, None, "Subscriber can be created from a dict (form) object")
        self.assertEqual(s.phone_number, "1234567890", "Subscriber can be created from a dict (form) object")

    def test_subscriber_combine_all_service_types(self):
        """
        Test subscriber with all service types
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="bulk,recycling,trash,")
        s.save()
        s = Subscriber.objects.all()[0]
        self.assertEqual(s.service_type, 'all', "Saving subscriber combines all service types into 'all'")

    def test_update_or_create_from_dict_previous_subscriber(self):
        """
        Test updating existing subscriber from a dict object
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", address="1104 Military St", service_type="all")
        s.save()
        s, error = Subscriber.update_or_create_from_dict( { "phone_number": "1234567890", "address": "7840 Van Dyke Pl", "service_type": "all" } )
        self.assertEqual(error, None, "Subscriber can be updated from a dict (form) object")
        self.assertEqual(s.waste_area_ids, ",8,", "Subscriber can be updated from a dict (form) object")

    def test_update_or_create_from_dict_invalid(self):
        """
        Test creating a subscriber from a dict object when dict is missing data
        """
        s, error = Subscriber.update_or_create_from_dict( { "waste_area_ids": "1", "service_type": "all" } )
        self.assertDictEqual(error, {"error": "address and phone_number are required"}, "Subscriber can only be created from a valid dict (form) object")
        self.assertEqual(s, None, "Subscriber can only be created from a valid dict (form) object")

    def test_waste_area_ids(self):
        """
        Test subscriber with one waste area id
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", service_type="all")
        s.save()

        self.assertEqual(s.waste_area_ids == ",1,", True)

    def test_multi_waste_area_ids(self):
        """
        Test subscriber with one waste area id
        """
        s = Subscriber(phone_number="2345678910", waste_area_ids="1,2,3", service_type="all")
        s.save()

        self.assertEqual(s.waste_area_ids == ",1,2,3,", True)

    def test_invalid_subscriber_data(self):

        INVALID_DATA = [
            { "phone_number": "234567891",    "waste_area_ids": "1,2,3", "service_type": "all" },
            { "phone_number": "2345678911",   "waste_area_ids": "x",     "service_type": "all" },
            { "phone_number": "2345678911",   "waste_area_ids": "",      "service_type": "all" },
            { "phone_number": "2345678912",   "waste_area_ids": "1,2,3", "service_type": "junk" },
            { "phone_number": "2345678912",   "waste_area_ids": "1,2,3", "service_type": "" },
            { "phone_number": "234-567-8912", "waste_area_ids": "1,2,3", "service_type": "" },
            { "phone_number": "",             "waste_area_ids": "1,2,3", "service_type": "" },
            { "phone_number": "234567891",   "waste_area_ids": "1,2,3", "service_type": "all", "status": "active" },
            { "phone_number": "2345678911",   "waste_area_ids": "1,2,3", "service_type": "all", "status": "" },
            { "phone_number": "2345678911",   "waste_area_ids": "1,2,3", "service_type": "all", "status": None },
            { "phone_number": "2345678911",   "waste_area_ids": "1,2,3", "service_type": "all", "status": "on" },
            { "phone_number": "2345678911",   "waste_area_ids": "1,2,3", "service_type": "all", "status": "off" },
            { "phone_number": "2345678911",   "waste_area_ids": "1,2,3", "service_type": "all" },
        ]

        for data in INVALID_DATA:
            subscriber = Subscriber(**data)
            with self.assertRaises(ValidationError, msg="Data '" + str(data) + "'' did not get validated properly") as error:
                subscriber.clean()

    def test_invalid_schedule_detail_data(self):

        INVALID_DATA = [
            { "detail_type": "infox",      "service_type": "all", "description": "test description", "normal_day": datetime.date(2017, 1, 1), "new_day": datetime.date(2017, 1, 2), "note": "test note", "waste_area_ids": "1" },
            { "detail_type": "",           "service_type": "all", "description": "test description", "normal_day": datetime.date(2017, 1, 1), "new_day": datetime.date(2017, 1, 2), "note": "test note", "waste_area_ids": "1" },
            { "detail_type": "info",       "service_type": "",    "description": "test description", "normal_day": datetime.date(2017, 1, 1), "new_day": datetime.date(2017, 1, 2), "note": "test note", "waste_area_ids": "1" },
            { "detail_type": "schedule",   "service_type": "all", "description": "test description", "normal_day": None,                      "new_day": datetime.date(2017, 1, 2), "note": "test note", "waste_area_ids": "1" },
            { "detail_type": "schedule",   "service_type": "all", "description": "test description", "normal_day": datetime.date(2017, 1, 2), "new_day": None,                      "note": "test note", "waste_area_ids": "1" },
            { "detail_type": "info",       "service_type": "all", "description": "test description", "normal_day": datetime.date(2017, 1, 1), "new_day": datetime.date(2017, 1, 2), "note": "test note", "waste_area_ids": "x" },
            { "detail_type": "start-date", "service_type": "all", "description": "test description", "normal_day": datetime.date(2017, 1, 1), "new_day": None,                      "note": "test note", "waste_area_ids": "1" },
            { "detail_type": "end-date",   "service_type": "all", "description": "test description", "normal_day": datetime.date(2017, 1, 1), "new_day": None,                      "note": "test note", "waste_area_ids": "1" },
        ]

        for data in INVALID_DATA:
            detail = ScheduleDetail(**data)
            with self.assertRaises(ValidationError, msg="Data '" + str(data) + "'' did not get validated properly") as error:
                detail.clean()

    def test_multiple_phone_numbers(self):
        """
        Verify our system can handle multiple phone numbers
        """
        phone_number = MsgHandler.get_phone_sender()
        self.assertTrue(phone_number and type(phone_number) is str, "get_phone_sender() should return a phone number")

    # Test some of the ScheduleDetail utility functions
    def test_get_date_week_type_a(self):
        self.assertEqual(ScheduleDetail.get_date_week_type(datetime.date(2017, 5, 4)), BiWeekType.A)

    def test_get_date_week_type_b(self):
        self.assertEqual(ScheduleDetail.get_date_week_type(datetime.date(2017, 5, 11)), BiWeekType.B)

    # Test actual API endpoints
    def test_subscribe_msg(self):

        c = Client()

        values = [
            ("all", {'received': '5005550006 - routes: ,0, - status: inactive - services: all (signed up via web)', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive bulk, recycling, trash and yard waste pickup reminders'}),
            ("trash", {'received': '5005550006 - routes: ,0, - status: inactive - services: trash (signed up via web)', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive trash pickup reminders'}),
            ("recycling", {'received': '5005550006 - routes: ,0, - status: inactive - services: recycling (signed up via web)', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive recycling pickup reminders'}),
            ("bulk,recycling,", {'received': '5005550006 - routes: ,0, - status: inactive - services: bulk,recycling, (signed up via web)', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive bulk, recycling and yard waste pickup reminders'}),
        ]

        for service, expected in values:
            cleanup_db()
            response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "address": "1104 Military St", "service_type": service } )
            self.assertEqual(response.status_code, 201)
            self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")
            self.assertEqual(Subscriber.objects.get(phone_number = "5005550006").status, 'inactive')

    # Test sign-up error-handling
    def test_subscribe_msg(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "500-555-0006", "address": "1104 Military St", "service_type": "all" } )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, {'error': 'phone_number must be 9 digits, no punctuation'}, "Subscription signup identifies invalid data")

    def test_confirm_subscription_msg(self):

        c = Client()

        values = [
            ("all", {'subscriber': '5005550006 - routes: ,0, - status: active - services: all', 'message': 'City of Detroit Public Works:  your bulk, recycling, trash and yard waste pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}),
            ("trash", {'subscriber': '5005550006 - routes: ,0, - status: active - services: trash', 'message': 'City of Detroit Public Works:  your trash pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}),
            ("recycling", {'subscriber': '5005550006 - routes: ,0, - status: active - services: recycling', 'message': 'City of Detroit Public Works:  your recycling pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}),
        ]

        for service, expected in values:
            cleanup_db()
            subscriber = Subscriber(phone_number="5005550006", waste_area_ids='0', address="1104 Military St", service_type=service)
            subscriber.save()

            response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
            self.assertEqual(response.status_code, 201)
            self.assertDictEqual(response.data, expected, "Subscription confirmation returns correct message")
            self.assertEqual(Subscriber.objects.get(phone_number = "5005550006").status, 'active')

    def test_confirm_deactivate(self):

        Subscriber(phone_number="5005550006", waste_area_ids='0', service_type='all', address="1104 Military St", status='active').save()

        c = Client()

        expected = {'subscriber': '5005550006 - routes: ,0, - status: inactive - services: all', 'message': 'City of Detroit Public Works:  your bulk, recycling, trash and yard waste pickup reminders have been cancelled (reply to this message at any time with ADD ME to start receiving reminders again)'}

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "REMOVE ME" } )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected, "Subscription confirmation returns correct message")
        self.assertEqual(Subscriber.objects.get(phone_number = "5005550006").status, 'inactive')

    def test_sign_up_by_fone(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/address/', { "From": "5005550006", "Body": "7840 van dyke pl" }, secure=True)
        self.assertEqual(response.status_code, 201)
        expected = {'subscriber': '5005550006 - routes: ,8, - status: active - services: all (signed up via text)', 'message': 'City of Detroit Public Works:  your bulk, recycling, trash and yard waste pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}
        self.assertDictEqual(response.data, expected, "Subscribing address returns correct message")

    def test_sign_up_by_fone_missing_number(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/address/', { "From": "", "Body": "7840 van dyke pl" }, secure=True)
        self.assertEqual(response.status_code, 400)

    def test_sign_up_by_fone_bad_address(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/address/', { "From": "5005550006", "Body": "invalid address" }, secure=True)
        self.assertEqual(response.status_code, 400)

    def test_sign_up_by_fone_city_included(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/address/', { "From": "5005550006", "Body": "7840 van dyke pl detroit, mi" }, secure=True)
        self.assertEqual(response.status_code, 201)
        expected = {'subscriber': '5005550006 - routes: ,8, - status: active - services: all (signed up via text)', 'message': 'City of Detroit Public Works:  your bulk, recycling, trash and yard waste pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}
        self.assertDictEqual(response.data, expected, "Subscribing address returns correct message")

    @skip('virginia park address not working yet')
    def test_sign_up_by_fone_virginia_park_st(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/address/', { "From": "5005550006", "Body": "670 virginia park st" }, secure=True)
        self.assertEqual(response.status_code, 201)
        expected = {'subscriber': '5005550006 - routes: ,8, - status: active - services: all (signed up via text)', 'message': 'City of Detroit Public Works:  your bulk, recycling, trash and yard waste pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}
        self.assertDictEqual(response.data, expected, "Subscribing address returns correct message")

    def test_sign_up_by_fone_vague_address(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/address/', { "From": "5005550006", "Body": "Detroit" }, secure=True)
        self.assertEqual(response.status_code, 400)

    def test_includes_yard_waste_all(self):
        self.assertTrue(views.includes_yard_waste(['all']))

    def test_includes_yard_waste_bulk(self):
        self.assertTrue(views.includes_yard_waste(['bulk']))

    def test_includes_yard_waste_year_round(self):
        self.assertTrue(views.includes_yard_waste(ScheduleDetail.YEAR_ROUND_SERVICES))

    def test_includes_yard_waste_trash(self):
        self.assertFalse(views.includes_yard_waste(['trash']))

    def test_add_additional_services_empty(self):
        self.assertEqual([], views.add_additional_services([], datetime.date(2017, 7, 1)))

    def test_add_additional_services_all(self):
        self.assertEqual(ScheduleDetail.YEAR_ROUND_SERVICES, views.add_additional_services(['all'], datetime.date(2017, 7, 1)))

    def test_add_additional_services(self):
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        services = views.add_additional_services(['bulk'], datetime.date(2017, 7, 1))
        self.assertListEqual(['bulk', 'yard waste'], services, "Yard waste, when active and bulk is getting picked up, gets added to list of services")

    def test_get_service_message(self):
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        message = views.get_service_message(['bulk'], datetime.date(2017, 7, 1))
        self.assertEqual(message, 'City of Detroit Public Works:  Your next pickup for bulk and yard waste is Saturday, July 01, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).')

    def test_get_service_message_note(self):
        detail = ScheduleDetail(detail_type='info', service_type='all', description='Please note that service will be unaffected by Christmas Day', normal_day=datetime.date(2016, 12, 25), note='Please put trash and recycling bins on the curb on normal schedule')
        detail.clean()
        detail.save(null_waste_area_ids=True)

        message = util.get_service_detail_message(['all'], detail)
        self.assertEqual(message, 'City of Detroit Public Works:  Please note that service will be unaffected by Christmas Day - Please put trash and recycling bins on the curb on normal schedule (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).')

    @mock.patch('slackclient.SlackClient.api_call')
    def test_slack_msg_handler(self, mocked_slackclient_api_call):

        mocked_slackclient_api_call.return_value = {'ok': True}

        previous_dry_run = SlackMsgHandler.DRY_RUN
        SlackMsgHandler.DRY_RUN = False
        self.assertTrue(SlackMsgHandler().send('test message'), "SlackMsgHandler.send() sends messages")
        SlackMsgHandler.DRY_RUN = previous_dry_run

    @mock.patch('slackclient.SlackClient.api_call')
    def test_slack_msg_handler_error(self, mocked_slackclient_api_call):

        mocked_slackclient_api_call.return_value = {'ok': False}

        previous_dry_run = SlackMsgHandler.DRY_RUN
        SlackMsgHandler.DRY_RUN = False
        self.assertFalse(SlackMsgHandler().send('test message'), "SlackMsgHandler.send() handles errors")
        SlackMsgHandler.DRY_RUN = previous_dry_run

    def test_get_waste_routes(self):
        """
        Verify we can look up waste routes by a given date
        """

        date = datetime.date(2017, 4, 21)
        for service_type in list(ScheduleDetail.SERVICE_ID_MAP.keys()):
            routes = ScheduleDetail.get_waste_routes(date, service_type)
            self.assertTrue(routes[8] == 'a', "Waste routes data should contain route 8 for {}".format(service_type))

    def test_get_waste_routes_offweek(self):
        """
        Verify we can look up waste routes by a given date
        """

        date = datetime.date(2017, 4, 28)
        for service_type in list(ScheduleDetail.SERVICE_ID_MAP.keys()):
            routes = ScheduleDetail.get_waste_routes(date, service_type)
            if service_type == ScheduleDetail.TRASH:
                self.assertEqual(routes[8], 'a', "Waste routes data should contain route 8 for {}".format(service_type))
            else:
                self.assertEqual(routes.get(8), None, "Waste routes data should not contain route 8 for {}".format(service_type))

    def test_subscribe_and_confirm(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "address": "16772 Sunderland Rd", "service_type": "all" } )
        self.assertEqual(response.status_code, 201)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
        self.assertEqual(response.status_code, 201)

        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.status, 'active')
        self.assertTrue(subscriber.last_status_update != None and subscriber.last_status_update != '')

    @skip('Blocking clients by IP not permitted by firewall')
    def test_subscribe_invalid_client(self):

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "From": "5005550006", "Body": "oops" } )
        self.assertEqual(response.status_code, 403, "/waste_notifier/subscribe/ blocks invalid callers")
        settings.ALLOWED_HOSTS.append("127.0.0.1")

    def test_subscribe_invalid_form(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "Body": "oops" } )
        self.assertEqual(response.status_code, 400, "/waste_notifier/subscribe/ rejects malformed content")

    def test_subscribe_invalid_address(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "address": "Invalid Address", "service_type": "all" } )
        self.assertEqual(response.status_code, 400, "/waste_notifier/subscribe/ rejects malformed content")

    def test_subscribe_extra_values(self):
        """
        Test creating a subscriber with extra values
        """

        c = Client()

        for value in [ 'latitude', 'longitude' ]:

            cleanup_db()
            response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "address": "7840 Van Dyke Pl", "service_type": "all", value: "test value" } )
            self.assertEqual(response.status_code, 201)
            subscriber = Subscriber.objects.all()[0]
            self.assertEqual(getattr(subscriber, value), 'test value', "Subscribing can set {}".format(value))

    def test_confirm_invalid_phone_number(self):

        c = Client()

        response = c.post('/waste_notifier/confirm/', { "From": "1111111111", "Body": "add me" } )
        self.assertEqual(response.status_code, 404, "/waste_notifier/confirm/ rejects invalid phone number")

    def test_confirm_invalid_form(self):

        c = Client()

        response = c.post('/waste_notifier/confirm/', { "Body": "add me" } )
        self.assertEqual(response.status_code, 400, "/waste_notifier/confirm/ rejects invalid form content")

    def test_invalid_confirm(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "address": "7840 Van Dyke pl", "service_type": "all" } )
        self.assertEqual(response.status_code, 201)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "oops" } )
        self.assertEqual(response.status_code, 201)

        subscriber = Subscriber.objects.first()

        self.assertEqual(subscriber.status, 'active', "User's status should be active (cos remove me not present)")
        self.assertEqual(subscriber.comment, "signed up via web - User's response to confirmation was: oops", "User's comment should contain their response")

    def test_invalid_confirm_sets_comment(self):

        c = Client()

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="0", address="1104 Military St", comment="test comment")
        subscriber.save()
        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "oops" } )

        subscriber = Subscriber.objects.first()
        self.assertTrue(subscriber.comment.find('test comment') == 0)
        self.assertTrue(subscriber.comment.find('oops') > 0)

    def test_subscribe_and_decline(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "address": "7840 Van Dyke Pl", "service_type": "all" } )
        self.assertEqual(response.status_code == 201, True)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "REMOVE ME" } )
        self.assertEqual(response.status_code == 201, True)

        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.status, 'inactive')
        self.assertTrue(subscriber.last_status_update != None and subscriber.last_status_update != '')

    def test_send_reminder(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="0", address="1104 Military St", service_type="all")
        subscriber.activate()

        # 20170522 is a monday - week 'b', so route 0 should get picked up
        response = views.send_notifications_request(date_val="20170522")
        expected = {'all': {0: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Monday, May 22, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}}
        expected = add_meta(expected, date=datetime.date(2017, 5, 22))
        self.assertDictEqual(expected, response, "Phone number did not get reminder")

    def test_send_info(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='all', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20180101")
        expected = {'citywide': {'subscribers': ['5005550006'], 'message': 'City of Detroit Public Works:  Special quarterly dropoff (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 1))
        self.assertDictEqual(expected, response, "Subscriber received info notification")

    def test_send_no_info(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20180102")
        expected = add_meta({}, date = datetime.date(2018, 1, 2))
        self.assertDictEqual(expected, response, "Phone number should not have gotten info")

    def test_send_info_all_services(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='all', description='City services have not been affected by snow storm', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = views.send_notifications_request(date_val="20180101")
        expected = {'citywide': {'message': 'City of Detroit Public Works:  City services have not been affected by snow storm (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 1))
        self.assertDictEqual(expected, response, "Sending info for all services works")

    def test_send_schedule_change(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20170407")
        expected = {'citywide': {'message': 'City of Detroit Public Works:  Pickups for recycling for the remainder of the week are postponed by 1 day due to test holiday (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}
        expected = add_meta(expected, date = datetime.date(2017, 4, 7))
        self.assertDictEqual(expected, response, "Phone number should have gotten recycling reschedule alert")

    def test_send_turkeyday_schedule_change1(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Thanksgiving', normal_day=datetime.date(2017, 11, 23), new_day=datetime.date(2017, 11, 24))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20171123")
        expected = {'citywide': {'message': 'City of Detroit Public Works:  Pickups for bulk, recycling and trash for the remainder of the week are postponed by 1 day due to Thanksgiving (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}
        expected = add_meta(expected, date = datetime.date(2017, 11, 23))
        self.assertDictEqual(expected, response, "Alerts during the week after thanksgiving get pushed back by 1 day")

    def test_send_turkeyday_schedule_change2(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Thanksgiving', normal_day=datetime.date(2017, 11, 23), new_day=datetime.date(2017, 11, 24))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20171124")
        expected = add_meta({}, date = datetime.date(2017, 11, 24))
        self.assertDictEqual(expected, response, "Alerts during the week after thanksgiving get pushed back by 1 day")

    def test_send_turkeyday_schedule_change3(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Thanksgiving', normal_day=datetime.date(2017, 11, 23), new_day=datetime.date(2017, 11, 24))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20171125")
        expected = {'trash': {8: {'message': 'City of Detroit Public Works:  Your next pickup for trash is Saturday, November 25, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}}
        expected = add_meta(expected, date = datetime.date(2017, 11, 25))
        self.assertDictEqual(expected, response, "Alerts during the week after thanksgiving get pushed back by 1 day")

    def test_send_no_schedule_change(self):

        # route 8 gets pickups on fridays, with recycling on 'a' weeks
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        # reschedule recycling citywide from friday to saturday for a 'b' week
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 14), new_day=datetime.date(2017, 4, 15))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()

        # now get pickup reminders for saturday
        response = views.send_notifications_request(date_val="20170408")
        expected = add_meta({}, date = datetime.date(2017, 4, 8))

        self.assertDictEqual(expected, response, "Phone number should not have gotten alert")

    def test_send_ab_onweek(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        response = views.send_notifications_request(date_val="20170407")
        expected = {'all': {8: {'subscribers': ['5005550006'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Friday, April 07, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}}
        expected = add_meta(expected, date=datetime.date(2017, 4, 7))
        self.assertDictEqual(expected, response, "Alerts for a/b onweek failed")

    def test_send_ab_offweek(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        # get a week where only trash should be pickup up
        response = views.send_notifications_request(date_val="20170526")
        expected = {'trash': {8: {'message': 'City of Detroit Public Works:  Your next pickup for trash is Friday, May 26, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}}
        expected = add_meta(expected, date=datetime.date(2017, 5, 26))
        self.assertDictEqual(expected, response, "Alerts for a/b offweek failed")

    def test_send_mix_days(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="12,14,22", address="16252 Wyoming St", service_type="all")
        subscriber.activate()

        date_results = {
            '20170417': {'all': {14: {'subscribers': ['5005550006'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Monday, April 17, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}},
            '20170418': {'all': {12: {'subscribers': ['5005550006'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Tuesday, April 18, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}},
            '20170419': {},
        }

        for date, expected in date_results.items():
            response = views.send_notifications_request(date_val=date)
            expected = add_meta(expected, date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])))

            self.assertDictEqual(expected, response, "Alerts for subscriber with mix of pickup days failed")

    def test_send_westside_wednesday_trash(self):

        subscriber = make_subscriber(address="1465 Chicago Blvd", service_type="all")

        response = views.send_notifications_request(date_val="20170419")
        expected = {'all': {11: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Wednesday, April 19, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}}
        expected = add_meta(expected, date=datetime.date(2017, 4, 19))
        self.assertDictEqual(expected, response, "Eastside wednesday trash residents should have gotten alerts")

    def test_send_westside_thursday_bulk_a(self):

        subscriber = make_subscriber(address="1465 Chicago Blvd", service_type="all")

        response = views.send_notifications_request(date_val="20170420")
        expected = {}
        expected = add_meta(expected, date=datetime.date(2017, 4, 20))
        self.assertDictEqual(expected, response, "Eastside thursday bulk A residents should have gotten alerts")

    def test_send_westside_thursday_recycling_b(self):

        subscriber = make_subscriber(address="1465 Chicago Blvd", service_type="all")

        response = views.send_notifications_request(date_val="20170413")
        expected = {}
        expected = add_meta(expected, date=datetime.date(2017, 4, 13))
        self.assertDictEqual(expected, response, "Eastside thursday recycling B residents should have gotten alerts")

    def test_send_bulk_yard_waste(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(today="20170504")
        # self.assertEqual(response.status_code, 200)
        expected = {'all': {8: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Friday, May 05, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}}
        expected = add_meta(expected, date=datetime.date(2017, 5, 5))
        self.assertDictEqual(expected, response, "Yard waste alerts get included whenever bulk pickup happens and yard waste pickup is active")

    def test_send_start_date(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts Monday, April 17, 2017', new_day=datetime.date(2017, 4, 17))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20170417")
        # self.assertEqual(response.status_code, 200)
        expected = {'citywide': {'message': 'City of Detroit Public Works:  Citywide yard waste pickup starts Monday, April 17, 2017 Monday, April 17, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}
        expected = add_meta(expected, date=datetime.date(2017, 4, 17))
        self.assertDictEqual(expected, response, "Yard waste start date alert should have been sent")

    def test_send_end_date(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts Monday, March 15, 2017', new_day=datetime.date(2017, 3, 15))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends friday, December 15, 2017', new_day=datetime.date(2017, 12, 15))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        response = views.send_notifications_request(date_val="20171215")
        # self.assertEqual(response.status_code, 200)
        expected = {'all': {8: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Friday, December 15, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}, 'citywide': {'message': 'City of Detroit Public Works:  Citywide yard waste pickup ends friday, December 15, 2017 Friday, December 15, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}
        expected = add_meta(expected, date=datetime.date(2017, 12, 15))
        self.assertDictEqual(expected, response, "Yard waste end date alert should have been sent")

    def test_send_auto(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        response = views.send_notifications_request()
        # self.assertEqual(response.status_code, 200)
        tomorrow = cod_utils.util.tomorrow()
        date_applicable = response['meta']['date_applicable']
        self.assertEqual(date_applicable, tomorrow.strftime("%Y-%m-%d"), "Auto-triggered alerts should run for tomorrow")

    def test_send_date_name_tomorrow(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        response = views.send_notifications_request(date_name="tomorrow")
        # self.assertEqual(response.status_code, 200)
        tomorrow = cod_utils.util.tomorrow()
        date_applicable = response['meta']['date_applicable']
        self.assertEqual(date_applicable, tomorrow.strftime("%Y-%m-%d"), "Alerts run with date name 'tomorrow' should run for tomorrow")

    def test_send_today_query_param(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        response = views.send_notifications_request(today="20170420")
        # self.assertEqual(response.status_code, 200)
        date_applicable = response['meta']['date_applicable']
        self.assertEqual(date_applicable, '2017-04-21', "Alerts run with 'today' passed in should run a day later")

    @skip("/waste_notifier/send/ POST no longer supported")
    def test_send_invalid_caller(self):

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.post('/waste_notifier/send/')
        self.assertEqual(response.status_code, 403, "/waste_notifier/send/ blocks invalid callers")

        settings.ALLOWED_HOSTS.append("127.0.0.1")

    @skip("/waste_notifier/send/ POST no longer supported")
    def test_send_invalid_query_param(self):

        c = Client()
        response = c.post('/waste_notifier/send/?invalid=true')
        self.assertEqual(response.status_code, 400, "/waste_notifier/send/ rejects invalid query params")

    def test_send_both_today_and_datename(self):

        response = views.send_notifications_request(date_name="tomorrow", today="20170101")
        # TODO finish this
        # self.assertEqual(response.status_code, 400, "/waste_notifier/send/ does not allow both today and tomorrow to be specified")

    def test_get_route_info(self):

        c = Client()
        response = c.get('/waste_notifier/route_info/')
        self.assertEqual(response.status_code, 200)



    #
    # Tests for new method of handling holidays (via ScheduleDetailMgr.get_day_routes(self, date))
    #

    def test_get_regular_week_routes(self):

        week_routes = ScheduleDetailMgr.instance().get_regular_week_routes(date = datetime.date(2017, 5, 5))
        expected = [{0: {'gid': 1, 'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 1: {'gid': 2, 'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 14: {'gid': 15, 'week': 'a', 'contractor': 'advance', 'services': 'all'}, 15: {'gid': 16, 'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {2: {'gid': 3, 'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 3: {'gid': 4, 'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 12: {'gid': 13, 'week': 'a', 'contractor': 'advance', 'services': 'all'}, 19: {'gid': 20, 'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {4: {'gid': 5, 'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 5: {'gid': 6, 'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 11: {'gid': 12, 'week': 'a', 'contractor': 'advance', 'services': 'all'}, 18: {'gid': 19, 'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {6: {'gid': 7, 'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'gid': 8, 'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 13: {'gid': 14, 'week': 'a', 'contractor': 'advance', 'services': 'all'}, 17: {'gid': 18, 'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {8: {'gid': 9, 'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 9: {'gid': 10, 'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 10: {'gid': 11, 'week': 'a', 'contractor': 'advance', 'services': 'all'}, 16: {'gid': 17, 'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {}, {}]
        expected = [{0: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 1: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 14: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 15: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {2: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 3: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 12: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 19: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {4: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 5: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 11: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 18: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {6: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 13: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 17: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {8: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 9: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 10: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 16: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {}, {}]
        self.assertEqual(week_routes.data, expected, "get_regular_week_routes() returns array of routes for a week")

    def test_get_week_schedule_changes_none(self):
        changes = ScheduleDetailMgr.instance().get_week_schedule_changes(date = datetime.date(2017, 5, 5))
        for key, value in changes.items():
            self.assertFalse(value, "get_week_schedule_changes() returns no schedule changes when there aren't any")

        # expected = {'20170505': [], '20170503': [], '20170507': [], '20170502': [], '20170501': [], '20170506': [], '20170504': []}
        # self.assertDictEqual(changes, expected, "get_week_schedule_changes() returns no schedule changes when there aren't any")

    def test_get_week_schedule_changes(self):
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        changes = ScheduleDetailMgr.instance().get_week_schedule_changes(date = datetime.date(2017, 5, 5))

        for key, value in changes.items():
            if key == '20170501':
                self.assertTrue(len(value) == 1)
                self.assertEqual(value[0].id, detail.id, "get_week_schedule_changes() returns schedule changes")
            else:
                self.assertFalse(value)

        # expected = {'20170505': [], '20170503': [], '20170507': [], '20170502': [], '20170501': ScheduleDetail.objects.filter(id=detail.id), '20170506': [], '20170504': []}
        # self.assertDictEqual(changes, expected, "get_week_schedule_changes() returns schedule changes")

    def test_get_route_specific_change(self):
        detail = ScheduleDetail(detail_type='schedule', waste_area_ids='0', service_type='all', description='flooding in SouthWest Detroit', normal_day=datetime.date(2017, 5, 5), new_day=datetime.date(2017, 5, 6))
        detail.clean()
        detail.save()
        make_subscriber(waste_area_ids='0')

        response = views.send_notifications_request(date_val="20170505")
        # self.assertEqual(response.status_code, 200)
        expected = {'0': {'message': 'City of Detroit Public Works:  Pickups for bulk, recycling and trash for the remainder of the week are postponed by 1 day due to flooding in SouthWest Detroit (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}}
        expected = add_meta(expected, date=datetime.date(2017, 5, 5))
        self.assertEqual(response, expected, "Schedule change can be made for specific route")

    def test_get_week_routes(self):

        week_routes = ScheduleDetailMgr.instance().get_week_routes(date = datetime.date(2017, 5, 5))
        expected = [{0: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 1: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 14: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 15: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {2: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 3: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 12: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 19: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {4: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 5: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 11: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 18: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {6: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 13: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 17: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {8: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 9: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 10: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 16: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {}, {}]
        self.assertEqual(week_routes.data, expected, "get_week_routes() returns array of routes for a week")

    def test_get_week_routes_holiday(self):

        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2019, 5, 1), new_day=datetime.date(2019, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        week_routes = ScheduleDetailMgr.instance().get_week_routes(date = datetime.date(2017, 5, 3))
        week_routes = week_routes.data
        expected = [{0: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 1: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 14: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 15: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {2: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 3: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 12: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 19: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {4: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 5: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 11: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 18: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {6: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 13: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 17: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {8: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 9: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 10: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 16: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}, {}, {}]
        self.assertEqual(week_routes, expected, "get_week_routes() reschedules array of routes for a week around holidays")

    def test_get_day_routes(self):

        routes = ScheduleDetailMgr.instance().get_day_routes(date = datetime.date(2017, 5, 5))
        expected = {8: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 9: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 10: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 16: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}
        self.assertEqual(routes, expected, "get_day_routes() returns routes for a date")

    def test_get_day_routes_holiday(self):

        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        routes = ScheduleDetailMgr.instance().get_day_routes(date = datetime.date(2017, 5, 5))
        expected = {6: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 13: {'week': 'a', 'contractor': 'advance', 'services': 'all'}, 17: {'week': 'b', 'contractor': 'advance', 'services': 'all'}}
        self.assertEqual(routes, expected, "get_day_routes() reschedules routes for a date if there is a holiday earlier in the week")

    def test_memorial_day_week(self):

        prior_dry_run = settings.DRY_RUN

        # create memorial day and yard waste schedule details
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Memorial Day', normal_day=datetime.date(2019, 5, 27), new_day=datetime.date(2019, 5, 28))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2019, 3, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2019, 12, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        # create subscribers for each day of week (note: memorial day 2017 occurs on an "A" week)
        sub_mon_a = make_subscriber(waste_area_ids='14', phone_number="5005550000")
        sub_mon_b = make_subscriber(waste_area_ids='0',  phone_number="5005550001")
        sub_tue_a = make_subscriber(waste_area_ids='2',  phone_number="5005550010")
        sub_tue_b = make_subscriber(waste_area_ids='19', phone_number="5005550011")
        sub_wed_a = make_subscriber(waste_area_ids='4',  phone_number="5005550020")
        sub_wed_b = make_subscriber(waste_area_ids='5',  phone_number="5005550021")
        sub_thu_a = make_subscriber(waste_area_ids='13', phone_number="5005550030")
        sub_thu_b = make_subscriber(waste_area_ids='17', phone_number="5005550031")
        sub_fri_a = make_subscriber(waste_area_ids='8',  phone_number="5005550040")
        sub_fri_b = make_subscriber(waste_area_ids='9',  phone_number="5005550041")

        values = [
            ( datetime.datetime(2019, 5, 26), {} ),
            ( datetime.datetime(2019, 5, 27), {'citywide': {'subscribers': ['5005550000', '5005550001', '5005550010', '5005550011', '5005550020', '5005550021', '5005550030', '5005550031', '5005550040', '5005550041'], 'message': 'City of Detroit Public Works:  Pickups for bulk, recycling, trash and yard waste for the remainder of the week are postponed by 1 day due to Memorial Day (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}} ),
            ( datetime.datetime(2019, 5, 28), {'trash': {0: {'message': 'City of Detroit Public Works:  Your next pickup for trash is Tuesday, May 28, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550001']}}, 'all': {14: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Tuesday, May 28, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550000']}}} ),
            ( datetime.datetime(2019, 5, 29), {'all':{2:{'message':'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Wednesday, May 29, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).','subscribers':['5005550010']}},'trash':{19:{'message':'City of Detroit Public Works:  Your next pickup for trash is Wednesday, May 29, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).','subscribers':['5005550011']}}} ),
            ( datetime.datetime(2019, 5, 30),  {'all': {4: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Thursday, May 30, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550020']}}, 'trash': {5: {'message': 'City of Detroit Public Works:  Your next pickup for trash is Thursday, May 30, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550021']}}} ),
            ( datetime.datetime(2019, 5, 31),  {'trash': {17: {'message': 'City of Detroit Public Works:  Your next pickup for trash is Friday, May 31, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550031']}}, 'all': {13: {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Friday, May 31, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550030']}}} ),
            ( datetime.datetime(2019, 6, 1),  {'trash': {9: {'subscribers': ['5005550041'], 'message': 'City of Detroit Public Works:  Your next pickup for trash is Saturday, June 01, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'meta': {'week_type': 'b', 'date_applicable': '2017-06-03', 'dry_run': True, 'current_time': '2017-05-25 17:43'}, 'all': {8: {'subscribers': ['5005550040'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Saturday, June 01, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}} ),
            ( datetime.datetime(2019, 6, 2), {} ),
        ]

        c = Client()

        for value in values:
            date = value[0].strftime("%Y%m%d")

            settings.DRY_RUN = True
            response = views.send_notifications_request(date_val=date)
            settings.DRY_RUN = prior_dry_run

            expected = add_meta(value[1], date=value[0])

            self.assertDictEqual(expected, response, "Memorial day week gets rescheduled properly")

    def test_holiday_multiple_routes(self):

        # create memorial day
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Memorial Day', normal_day=datetime.date(2017, 5, 29), new_day=datetime.date(2017, 5, 30))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        subscriber = make_subscriber(waste_area_ids='14,27,31')

        c = Client()

        with patch.object(MsgHandler, 'send_text', return_value=True) as mock_send_text:
            response = views.send_notifications_request(date_val="20170529")

        mock_send_text.assert_called_once_with(phone_number='5005550006', text='City of Detroit Public Works:  Pickups for bulk, recycling and trash for the remainder of the week are postponed by 1 day due to Memorial Day (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', dry_run_param=True)

    def test_format_slack_alerts_summary(self):
        content = {'trash': {11: {'subscribers': ['3136102012', '9174538684', '3135068800', '2484992308', '2676300369', '3133202044', '5869133397', '3134923996', '2679700026', '5863228964', '3137062742', '3135504576', '3138190143', '3138080122', '7347485413', '3138025608', '2487015166', '3134546860', '3134832492', '3138623021', '3133198115', '3137015482', '3132058535', '3133462045', '2489104129', '3134737118'], 'message': 'City of Detroit Public Works:  Your next pickup for trash is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}, 5: {'subscribers': ['3138504195', '3135803973'], 'message': 'City of Detroit Public Works:  Your next pickup for trash is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'all': {4: {'subscribers': ['5865638822', '3135498078', '3137195691', '3137581842', '3137587477'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'meta': {'date_applicable': '2017-05-31', 'dry_run': True, 'week_type': 'b', 'current_time': '2017-05-26 10:51'}, 'recycling': {22: {'subscribers': ['3134495504', '3133201794', '3134780304', '3134150028', '3134617273'], 'message': 'City of Detroit Public Works:  Your next pickup for recycling is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'bulk': {34: {'subscribers': ['8109624844', '3132084486', '3137283175', '3136139213', '3134784213'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk and yard waste is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}}
        summary = format_slack_alerts_summary(content)
        expected = 'DPW Waste Pickup Reminder Summary:\n\nall\n\troute 4 - 5 reminders\nbulk\n\troute 34 - 5 reminders\nrecycling\n\troute 22 - 5 reminders\ntrash\n\troute 5 - 2 reminders\n\troute 11 - 26 reminders\n\nTotal reminders sent out:  43'

        self.assertEqual(summary, expected, "format_slack_alerts_summary() formats notifications summary correctly")

    def test_send_info_msg(self):

        waste_area_id_sets = [ "14,27,31", "8" ]
        dates = [ datetime.date(2017, 12, 2), datetime.date(2017, 12, 4) ]
        expected = 'City of Detroit Public Works:  Curbside yard waste pickup will be suspended after Dec 15 until next spring. - Please set out yard waste in paper lawn bags or in 32-gallon containers labelled YARD WASTE ONLY the night before your pickup. (See http://www.detroitmi.gov/publicworks for more details.) (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'

        for waste_area_ids in waste_area_id_sets:

            for date in dates:

                cleanup_db()

                subscriber = Subscriber(phone_number="5005550006", waste_area_ids=waste_area_ids, address="7840 Van Dyke Pl", service_type="all")
                subscriber.activate()
                detail = ScheduleDetail(detail_type='info', service_type='all', description='Curbside yard waste pickup will be suspended after Dec 15 until next spring.', note='Please set out yard waste in paper lawn bags or in 32-gallon containers labelled YARD WASTE ONLY the night before your pickup. (See http://www.detroitmi.gov/publicworks for more details.)', normal_day=date)
                detail.clean()
                detail.save(null_waste_area_ids=True)

                response = views.send_notifications_request(date_val=date.strftime("%Y%m%d"))
                self.assertEqual(response['citywide']['message'], expected, "Information can be sent out")

    def test_send_reminders_2019(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", address="7840 Van Dyke Pl", service_type="all")
        subscriber.activate()

        expected = {'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Friday, January 11, 2019 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).', 'subscribers': ['5005550006']}
        response = views.send_notifications_request(date_val=datetime.date(2019, 1, 11).strftime("%Y%m%d"))
        self.assertEqual(response['all'][8], expected, "Information can be sent out")

    def test_get_alexa_service_info(self):

        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Christmas', normal_day=datetime.date(2017, 12, 25), new_day=datetime.date(2017, 12, 26))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        today = "20171129"

        c = Client()
        response = c.get("/waste_notifier/address/7840 Van Dyke Pl/{}/".format(today), secure=True)

        tomorrow = '2017-12-01T00:00:00.000'

        expected = {
            "next_pickups": {
                ScheduleDetail.RECYCLING : { "date": tomorrow, "provider": "gfl" },
                ScheduleDetail.BULK : { "date": tomorrow, "provider": "gfl" },
                ScheduleDetail.TRASH : { "date": tomorrow, "provider": "gfl" }
            },
            "details": { "schedule": [{
                    'description': 'Christmas',
                    'newDay': '2017-12-26T00:00:00.000',
                    'normalDay': '2017-12-25T00:00:00.000',
                    'note': None,
                    'service': 'all',
                    'wasteAreaIds': ''
                }]
            },
            "all_services": ["trash", "recycling", "bulk", "yard waste"]
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected, response.data, "Individual resident can request next service date")

    def test_get_alexa_service_info_alt_week(self):

        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Christmas', normal_day=datetime.date(2017, 12, 25), new_day=datetime.date(2017, 12, 26))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        today = "20171221"

        c = Client()
        response = c.get("/waste_notifier/address/7840 Van Dyke Pl/{}/".format(today), secure=True)

        tomorrow = '2017-12-22T00:00:00.000'

        # reschedule for next week due to alt week and 1 day late due to holiday
        next_week = '2017-12-30T00:00:00.000'

        expected = {
            "next_pickups": {
                ScheduleDetail.RECYCLING : { "date": next_week, "provider": "gfl" },
                ScheduleDetail.BULK : { "date": next_week, "provider": "gfl" },
                ScheduleDetail.TRASH : { "date": tomorrow, "provider": "gfl" }
            },
            "details": { "schedule": [{
                    'description': 'Christmas',
                    'newDay': '2017-12-26T00:00:00.000',
                    'normalDay': '2017-12-25T00:00:00.000',
                    'note': None,
                    'service': 'all',
                    'wasteAreaIds': ''
                }]
            },
            "all_services": ["trash", "recycling", "bulk", "yard waste"]
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected, response.data, "Individual resident can request next service date")

    def test_get_alexa_service_info_holiday(self):

        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 15))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='Christmas', normal_day=datetime.date(2017, 12, 25), new_day=datetime.date(2017, 12, 26))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        today = "20171228"

        c = Client()
        response = c.get("/waste_notifier/address/7840 Van Dyke Pl/{}/".format(today), secure=True)

        tomorrow = '2017-12-30T00:00:00.000'

        expected = {
            "next_pickups": {
                ScheduleDetail.RECYCLING : { "date": tomorrow, "provider": "gfl" },
                ScheduleDetail.BULK : { "date": tomorrow, "provider": "gfl" },
                ScheduleDetail.TRASH : { "date": tomorrow, "provider": "gfl" }
            },
            'all_services': [
                'trash',
                'recycling',
                'bulk',
                'yard waste'
            ],
            'details': {}
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected, response.data, "Individual resident can request next service date")

    def test_get_alexa_service_info_bad_address(self):

        c = Client()

        response = c.get('/waste_notifier/address/bad/', secure=True)
        self.assertEqual(response.status_code, 400)

    def test_get_alexa_service_info_insecure(self):

        c = Client()

        response = c.get('/waste_notifier/address/7840 Van Dyke Pl/')
        self.assertEqual(response.status_code, 403)

    def test_slack_waste_notifier_messages(self):

        slack_handler = WasteNotifierSlackHandler()
        slack_handler.slack_alerts_start()
        slack_handler.slack_alerts_update(msg_cnt=1000)

        content = {'trash': {11: {'subscribers': ['3136102012', '9174538684', '3135068800', '2484992308', '2676300369', '3133202044', '5869133397', '3134923996', '2679700026', '5863228964', '3137062742', '3135504576', '3138190143', '3138080122', '7347485413', '3138025608', '2487015166', '3134546860', '3134832492', '3138623021', '3133198115', '3137015482', '3132058535', '3133462045', '2489104129', '3134737118'], 'message': 'City of Detroit Public Works:  Your next pickup for trash is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}, 5: {'subscribers': ['3138504195', '3135803973'], 'message': 'City of Detroit Public Works:  Your next pickup for trash is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'all': {4: {'subscribers': ['5865638822', '3135498078', '3137195691', '3137581842', '3137587477'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk, recycling, trash and yard waste is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'meta': {'date_applicable': '2017-05-31', 'dry_run': True, 'week_type': 'b', 'current_time': '2017-05-26 10:51'}, 'recycling': {22: {'subscribers': ['3134495504', '3133201794', '3134780304', '3134150028', '3134617273'], 'message': 'City of Detroit Public Works:  Your next pickup for recycling is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}, 'bulk': {34: {'subscribers': ['8109624844', '3132084486', '3137283175', '3136139213', '3134784213'], 'message': 'City of Detroit Public Works:  Your next pickup for bulk and yard waste is Wednesday, May 31, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).'}}}
        slack_handler.slack_alerts_summary(content=content)
