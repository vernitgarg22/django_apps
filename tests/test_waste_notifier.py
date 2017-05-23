import datetime

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

import mock

import cod_utils.util
import cod_utils.security
import tests.disabled

from waste_notifier.models import Subscriber
from waste_notifier.util import *
from waste_schedule.models import ScheduleDetail, BiWeekType
from waste_schedule.schedule_detail_mgr import ScheduleDetailMgr

from waste_notifier import views


def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(Subscriber)
    cleanup_model(ScheduleDetail)


def add_meta(content, date = cod_utils.util.tomorrow()):
    """
    Add meta data for the /send endpoint (e.g., date)
    """

    week_type = ScheduleDetail.get_date_week_type(datetime.date.today())
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
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", service_type="all")
        s.save()
        views.add_subscriber_comment("1234567890", "testing")
        s = Subscriber.objects.all()[0]
        self.assertTrue(str(s).find("testing"), "add_subscriber_comment() adds a comment to the subscriber")

    def test_subscriber_delete(self):
        """
        Verify that deleting a subscriber does a 'soft delete'
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", service_type="all")
        s.delete()
        self.assertEqual(s.status, 'inactive', "Deleting a subscriber causes a 'soft delete'")

    def test_update_or_create_from_dict(self):
        """
        Test creating a subscriber from a dict object
        """
        s, error = Subscriber.update_or_create_from_dict( { "phone_number": "1234567890", "waste_area_ids": "1", "service_type": "all" } )
        self.assertEqual(error, None, "Subscriber can be created from a dict (form) object")
        self.assertEqual(s.phone_number, "1234567890", "Subscriber can be created from a dict (form) object")

    def test_subscriber_combine_all_service_types(self):
        """
        Test subscriber with all service types
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", service_type="bulk,recycling,trash,")
        s.save()
        s = Subscriber.objects.all()[0]
        self.assertEqual(s.service_type, 'all', "Saving subscriber combines all service types into 'all'")

    def test_update_or_create_from_dict_previous_subscriber(self):
        """
        Test updating existing subscriber from a dict object
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", service_type="all")
        s.save()
        s, error = Subscriber.update_or_create_from_dict( { "phone_number": "1234567890", "waste_area_ids": "2", "service_type": "all" } )
        self.assertEqual(error, None, "Subscriber can be updated from a dict (form) object")
        self.assertEqual(s.waste_area_ids, ",2,", "Subscriber can be updated from a dict (form) object")

    def test_update_or_create_from_dict_invalid(self):
        """
        Test creating a subscriber from a dict object when dict is missing data
        """
        s, error = Subscriber.update_or_create_from_dict( { "waste_area_ids": "1", "service_type": "all" } )
        self.assertDictEqual(error, {"error": "phone_number and waste_area_ids are required"}, "Subscriber can only be created from a valid dict (form) object")
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
        phone_number = cod_utils.util.MsgHandler.get_phone_sender()
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
            ("all", {'received': '5005550006 - routes: ,0, - status: inactive - services: all', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive bulk, recycling, trash and yard waste pickup reminders'}),
            ("trash", {'received': '5005550006 - routes: ,0, - status: inactive - services: trash', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive trash pickup reminders'}),
            ("recycling", {'received': '5005550006 - routes: ,0, - status: inactive - services: recycling', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive recycling pickup reminders'}),
            ("bulk,recycling,", {'received': '5005550006 - routes: ,0, - status: inactive - services: bulk,recycling,', 'message': 'City of Detroit Public Works:  reply with ADD ME to confirm that you want to receive bulk, recycling and yard waste pickup reminders'}),
        ]

        for service, expected in values:
            cleanup_db()
            response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "0", "service_type": service } )
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")


    def test_confirm_subscription_msg(self):

        c = Client()

        values = [
            ("all", {'subscriber': '5005550006 - routes: ,0, - status: active - services: all', 'message': 'City of Detroit Public Works:  your bulk, recycling, trash and yard waste pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}),
            ("trash", {'subscriber': '5005550006 - routes: ,0, - status: active - services: trash', 'message': 'City of Detroit Public Works:  your trash pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}),
            ("recycling", {'subscriber': '5005550006 - routes: ,0, - status: active - services: recycling', 'message': 'City of Detroit Public Works:  your recycling pickup reminders have been confirmed\n(reply REMOVE ME to any of the reminders to stop receiving them)'}),
        ]

        for service, expected in values:
            cleanup_db()
            subscriber = Subscriber(phone_number="5005550006", waste_area_ids='0', service_type=service)
            subscriber.save()

            response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.data, expected, "Subscription confirmation returns correct message")


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
        self.assertEqual(message, 'City of Detroit Public Works:  Your next pickup for bulk and yard waste is Jul 01, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).')

    @mock.patch('requests.post')
    def test_slack_msg_handler(self, mocked_requests_post):

        mocked_requests_post.return_value.status_code = 200

        previous_dry_run = SlackMsgHandler.DRY_RUN
        SlackMsgHandler.DRY_RUN = False
        self.assertTrue(SlackMsgHandler().send('test message'), "SlackMsgHandler.send() sends messages")
        SlackMsgHandler.DRY_RUN = previous_dry_run

    @mock.patch('requests.post')
    def test_slack_msg_handler_error(self, mocked_requests_post):

        mocked_requests_post.return_value.status_code = 500

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

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code, 200)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
        self.assertEqual(response.status_code, 200)

        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.status, 'active')
        self.assertTrue(subscriber.last_status_update != None and subscriber.last_status_update != '')

    def test_subscribe_invalid_client(self):

        # Force block_client to block us
        cod_utils.security.API_CLIENT_WHITELIST.remove("127.0.0.1")

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "From": "5005550006", "Body": "oops" } )
        self.assertEqual(response.status_code, 403, "/waste_notifier/subscribe/ blocks invalid callers")
        cod_utils.security.API_CLIENT_WHITELIST.append("127.0.0.1")

    def test_subscribe_invalid_form(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "Body": "oops" } )
        self.assertEqual(response.status_code, 400, "/waste_notifier/subscribe/ rejects malformed content")

    def test_subscribe_extra_values(self):
        """
        Test creating a subscriber with extra values
        """

        c = Client()

        for value in [ 'address', 'latitude', 'longitude' ]:

            cleanup_db()
            response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all", value: "test value" } )
            self.assertEqual(response.status_code, 200)
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

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code, 200)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "oops" } )
        self.assertEqual(response.status_code, 200)

        subscriber = Subscriber.objects.first()

        self.assertEqual(subscriber.status, 'active', "User's status should be active (cos remove me not present)")
        self.assertEqual(subscriber.comment, "User's response to confirmation was: oops", "User's comment should contain their response")

    def test_invalid_confirm_sets_comment(self):

        c = Client()

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="0", comment="test comment")
        subscriber.save()
        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "oops" } )

        subscriber = Subscriber.objects.first()
        self.assertTrue(subscriber.comment.find('test comment') == 0)
        self.assertTrue(subscriber.comment.find('oops') > 0)

    def test_subscribe_and_decline(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code == 200, True)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "REMOVE ME" } )
        self.assertEqual(response.status_code == 200, True)

        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.status, 'inactive')
        self.assertTrue(subscriber.last_status_update != None and subscriber.last_status_update != '')

    def test_send_reminder(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="0", service_type="all")
        subscriber.activate()

        c = Client()

        # 20170522 is a monday - week 'b', so route 0 should get picked up
        response = c.post('/waste_notifier/send/20170522/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'all': {0: {'5005550006': 1}, 1: {}}, 'citywide': {}, 'recycling': {26: {}}, 'bulk': {30: {}}, 'trash': {14: {}}}, date=datetime.date(2017, 5, 22))
        self.assertDictEqual(expected, response.data, "Phone number did not get reminder")

    def test_send_info(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20180101/')
        self.assertEqual(response.status_code, 200)
        expected = {'bulk': {29: {}}, 'all': {0: {}, 1: {}}, 'citywide': {'5005550006': 1}, 'recycling': {27: {}}, 'trash': {14: {}}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 1))
        self.assertDictEqual(expected, response.data, "Phone number did not get info")

    def test_send_no_info(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20180102/')
        self.assertEqual(response.status_code, 200)
        expected = {'recycling': {24: {}, 25: {}}, 'all': {2: {}, 3: {}}, 'bulk': {31: {}}, 'citywide': {}, 'trash': {13: {}}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 2))
        self.assertDictEqual(expected, response.data, "Phone number should not have gotten info")

    def test_send_info_all_services(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='all', description='City services have not affected by snow storm', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20180101/')
        self.assertEqual(response.status_code, 200)
        expected = {'bulk': {29: {}}, 'meta': {'week_type': 'b', 'current_time': '2017-05-22 13:35', 'dry_run': True, 'date_applicable': '2018-01-01'}, 'trash': {14: {}}, 'recycling': {27: {}}, 'all': {1: {}}, 'citywide': {'5005550006': 1}}
        expected = {'bulk': {29: {}}, 'meta': {'week_type': 'b', 'current_time': '2017-05-22 15:00', 'dry_run': True, 'date_applicable': '2018-01-01'}, 'trash': {14: {}}, 'citywide': {'5005550006': 1}, 'recycling': {27: {}}, 'all': {0: {}, 1: {}}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 1))
        self.assertDictEqual(expected, response.data, "Sending info for all services works")

    def test_send_schedule_change(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20170407/')
        self.assertEqual(response.status_code, 200)
        expected = {'recycling': {16: {}}, 'trash': {10: {}}, 'all': {8: {'5005550006': 1}, 9: {}}, 'citywide': {}, 'bulk': {38: {}}}
        expected = add_meta(expected, date = datetime.date(2017, 4, 7))
        self.assertDictEqual(expected, response.data, "Phone number should have gotten recycling reschedule alert")

    def test_send_no_schedule_change(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20170408/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'citywide': {}}, date = datetime.date(2017, 4, 8))
        self.assertDictEqual(expected, response.data, "Phone number should not have gotten alert")

    def test_send_ab_onweek(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170407/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'bulk': {38: {}}, 'recycling': {16: {}}, 'citywide': {}, 'all': {8: {'5005550006': 1}, 9: {}}, 'trash': {10: {}}}, date=datetime.date(2017, 4, 7))
        self.assertDictEqual(expected, response.data, "Alerts for a/b onweek failed")

    def test_send_ab_offweek(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170414/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'citywide': {}, 'recycling': {15: {}}, 'trash': {10: {}}, 'bulk': {37: {}}, 'all': {8: {'5005550006': 1}, 9: {}}}, date=datetime.date(2017, 4, 14))
        self.assertDictEqual(expected, response.data, "Alerts for a/b offweek failed")

    def test_send_mix_days(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="12,14,22", service_type="all")
        subscriber.activate()

        c = Client()
        date_results = {
            '20170417': {'all': {0: {}, 1: {}}, 'recycling': {27: {}}, 'citywide': {}, 'bulk': {29: {}}, 'trash': {14: {'5005550006': 1}}},
            '20170418': {'trash': {13: {}}, 'bulk': {31: {}}, 'citywide': {}, 'all': {2: {}, 3: {}}, 'recycling': {24: {}, 25: {}}},
            '20170419': {'recycling': {21: {}, 22: {'5005550006': 1}}, 'trash': {11: {}}, 'citywide': {}, 'bulk': {34: {}}, 'all': {4: {}, 5: {}}},
        }

        for date, expected in date_results.items():
            response = c.post("/waste_notifier/send/{}/".format(date))
            self.assertEqual(response.status_code, 200)
            expected = add_meta(expected, date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])))
            self.assertDictEqual(expected, response.data, "Alerts for subscriber with mix of pickup days failed")

    def test_send_eastside_wednesday_trash(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="11,28,35", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170419/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'trash': {11: {'5005550006': 1}}, 'all': {4: {}, 5: {}}, 'citywide': {}, 'bulk': {34: {}}, 'recycling': {21: {}, 22: {}}}, date=datetime.date(2017, 4, 19))
        self.assertDictEqual(expected, response.data, "Eastside wednesday trash residents should have gotten alerts")

    def test_send_eastside_thursday_bulk_a(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="11,28,35", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170420/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'citywide': {}, 'recycling': {17: {}, 18: {}}, 'trash': {12: {}}, 'bulk': {35: {'5005550006': 1}}, 'all': {6: {}, 7: {}}}, date=datetime.date(2017, 4, 20))
        self.assertDictEqual(expected, response.data, "Eastside thursday bulk A residents should have gotten alerts")

    def test_send_eastside_thursday_recycling_b(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="11,28,35", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170413/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'all': {6: {}, 7: {}}, 'recycling': {28: {'5005550006': 1}}, 'citywide': {}, 'trash': {12: {}}, 'bulk': {36: {}}}, date=datetime.date(2017, 4, 13))
        self.assertDictEqual(expected, response.data, "Eastside thursday recycling B residents should have gotten alerts")

    def test_send_bulk_yard_waste(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/?today=20170504')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'all': {8: {'5005550006': 1}, 9: {}}, 'bulk': {38: {}}, 'trash': {10: {}}, 'recycling': {16: {}}, 'citywide': {}}, date=datetime.date(2017, 5, 5))
        self.assertDictEqual(expected, response.data, "Yard waste alerts get included whenever bulk pickup happens and yard waste pickup is active")

    def test_send_start_date(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts monday, April 17, 2017', new_day=datetime.date(2017, 4, 17))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20170417/')
        self.assertEqual(response.status_code, 200)
        expected = {'all': {0: {}, 1: {}}, 'bulk': {29: {}}, 'citywide': {'5005550006': 1}, 'trash': {14: {}}, 'recycling': {27: {}}}
        expected = add_meta(expected, date=datetime.date(2017, 4, 17))
        self.assertDictEqual(expected, response.data, "Yard waste start date alert should have been sent")

    def test_send_end_date(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends friday, December 15, 2017', new_day=datetime.date(2017, 12, 15))
        detail.clean()
        detail.save(null_waste_area_ids=True)

        c = Client()
        response = c.post('/waste_notifier/send/20171215/')
        self.assertEqual(response.status_code, 200)
        expected = {'recycling': {8: {'5005550006': 1}, 16: {}}, 'bulk': {8: {'5005550006': 1}, 38: {}}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'citywide': {'5005550006': 1}}
        expected = {'all': {8: {'5005550006': 1}, 9: {}}, 'trash': {10: {}}, 'citywide': {'5005550006': 1}, 'bulk': {38: {}}, 'recycling': {16: {}}}
        expected = add_meta(expected, date=datetime.date(2017, 12, 15))
        self.assertDictEqual(expected, response.data, "Yard waste end date alert should have been sent")

    def test_send_auto(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/')
        self.assertEqual(response.status_code, 200)
        tomorrow = cod_utils.util.tomorrow()
        date_applicable = response.data['meta']['date_applicable']
        self.assertEqual(date_applicable, tomorrow.strftime("%Y-%m-%d"), "Auto-triggered alerts should run for tomorrow")

    def test_send_date_name_tomorrow(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/tomorrow/')
        self.assertEqual(response.status_code, 200)
        tomorrow = cod_utils.util.tomorrow()
        date_applicable = response.data['meta']['date_applicable']
        self.assertEqual(date_applicable, tomorrow.strftime("%Y-%m-%d"), "Alerts run with date name 'tomorrow' should run for tomorrow")

    def test_send_today_query_param(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/?today=20170420')
        self.assertEqual(response.status_code, 200)
        date_applicable = response.data['meta']['date_applicable']
        self.assertEqual(date_applicable, '2017-04-21', "Alerts run with 'today' passed in should run a day later")

    def test_send_invalid_caller(self):

        # Force block_client to block us
        cod_utils.security.API_CLIENT_WHITELIST.remove("127.0.0.1")

        c = Client()
        response = c.post('/waste_notifier/send/')
        self.assertEqual(response.status_code, 403, "/waste_notifier/send/ blocks invalid callers")

        cod_utils.security.API_CLIENT_WHITELIST.append("127.0.0.1")

    def test_send_invalid_query_param(self):

        c = Client()
        response = c.post('/waste_notifier/send/?invalid=true')
        self.assertEqual(response.status_code, 400, "/waste_notifier/send/ rejects invalid query params")

    def test_send_both_today_and_datename(self):

        c = Client()
        response = c.post('/waste_notifier/send/tomorrow/?today=20170101')
        self.assertEqual(response.status_code, 400, "/waste_notifier/send/ does not allow both today and tomorrow to be specified")

    def test_get_route_info(self):

        c = Client()
        response = c.get('/waste_notifier/route_info/')
        self.assertEqual(response.status_code, 200)



    #
    # Tests for new method of handling holidays (via ScheduleDetailMgr.get_day_routes(self, date))
    #

    def test_get_regular_week_routes(self):
        week_routes = ScheduleDetailMgr.instance().get_regular_week_routes(date = datetime.date(2017, 5, 5))
        expected = [{0: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 1: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 27: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 29: {'week': 'a', 'contractor': 'advance', 'services': 'bulk'}, 14: {'week': ' ', 'contractor': 'advance', 'services': 'trash'}}, {2: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 3: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 24: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 25: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 13: {'week': ' ', 'contractor': 'advance', 'services': 'trash'}, 31: {'week': 'a', 'contractor': 'advance', 'services': 'bulk'}}, {34: {'week': 'a', 'contractor': 'advance', 'services': 'bulk'}, 4: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 5: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 22: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 11: {'week': ' ', 'contractor': 'advance', 'services': 'trash'}, 21: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}}, {17: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 18: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 35: {'week': 'a', 'contractor': 'advance', 'services': 'bulk'}, 6: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 12: {'week': ' ', 'contractor': 'advance', 'services': 'trash'}}, {8: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 9: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 10: {'week': ' ', 'contractor': 'advance', 'services': 'trash'}, 38: {'week': 'a', 'contractor': 'advance', 'services': 'bulk'}, 16: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}}, {}, {}]
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

    def test_get_week_routes(self):
        week_routes = ScheduleDetailMgr.instance().get_week_routes(date = datetime.date(2017, 5, 5))
        expected = [{1: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 27: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 29: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 14: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}}, {24: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 25: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 2: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 13: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 31: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}}, {34: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 11: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 4: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 21: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 22: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}}, {17: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 18: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 35: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 12: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 7: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}}, {8: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 16: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 10: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 38: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}}, {}, {}]
        expected = [{0: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 1: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 27: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 29: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 14: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}}, {2: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 3: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 24: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 25: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 13: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 31: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}}, {34: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 4: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 5: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 22: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 11: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 21: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}}, {17: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 18: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 35: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 6: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 7: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 12: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}}, {8: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 9: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 10: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 38: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 16: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}}, {}, {}]
        self.assertEqual(week_routes.data, expected, "get_week_routes() returns array of routes for a week")

    def test_get_week_routes_holiday(self):
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        week_routes = ScheduleDetailMgr.instance().get_week_routes(date = datetime.date(2017, 5, 5))
        week_routes = week_routes.data
        expected = [{}, {0: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 1: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 27: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 29: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 14: {'contractor': 'advance', 'services': 'trash', 'week': ' '}}, {2: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 3: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 24: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 25: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 13: {'contractor': 'advance', 'services': 'trash', 'week': ' '}, 31: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}}, {34: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 4: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 5: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 22: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 11: {'contractor': 'advance', 'services': 'trash', 'week': ' '}, 21: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}}, {17: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 18: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 35: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 6: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 7: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 12: {'contractor': 'advance', 'services': 'trash', 'week': ' '}}, {8: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 9: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 10: {'contractor': 'advance', 'services': 'trash', 'week': ' '}, 38: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 16: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}}, {}]
        self.assertEqual(week_routes, expected, "get_week_routes() reschedules array of routes for a week around holidays")

    def test_get_day_routes(self):
        routes = ScheduleDetailMgr.instance().get_day_routes(date = datetime.date(2017, 5, 5))
        expected = {8: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 9: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 10: {'contractor': 'advance', 'services': 'trash', 'week': ' '}, 38: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 16: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}}
        self.assertEqual(routes, expected, "get_day_routes() returns routes for a date")

    def test_get_day_routes_holiday(self):
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        routes = ScheduleDetailMgr.instance().get_day_routes(date = datetime.date(2017, 5, 5))
        expected = {17: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 18: {'week': 'a', 'contractor': 'advance', 'services': 'recycle'}, 35: {'week': 'a', 'contractor': 'advance', 'services': 'bulk'}, 6: {'week': 'b', 'contractor': 'gfl', 'services': 'all'}, 7: {'week': 'a', 'contractor': 'gfl', 'services': 'all'}, 12: {'week': ' ', 'contractor': 'advance', 'services': 'trash'}}
        self.assertEqual(routes, expected, "get_day_routes() reschedules routes for a date if there is a holiday earlier in the week")

    def test_format_slack_alerts_summary(self):
        content = {"recycling":{28:{"3136102012":1,"2676300369":1,"3138190143":1,"7347485413":1,"3134923996":1,"3135504576":1},6:{"3136575302":1}},"trash":{12:{"3132281121":1},6:{"3136575302":1},7:{"5863440535":1}},"citywide":{},"meta":{"date_applicable":"2017-05-11","dry_run":False,"week_type":"b","current_time":"2017-05-10 18:00"},"bulk":{36:{"3134923996":1,"3138025608":1,"7347485413":1,"3133202044":1},6:{"3136575302":1}}}
        summary = format_slack_alerts_summary(content)
        expected = 'DPW Waste Pickup Reminder Summary:\n\nbulk\n\troute 6 - 1 reminders\n\troute 36 - 4 reminders\nrecycling\n\troute 6 - 1 reminders\n\troute 28 - 6 reminders\ntrash\n\troute 6 - 1 reminders\n\troute 7 - 1 reminders\n\troute 12 - 1 reminders\n\nTotal reminders sent out:  11'
        self.assertEqual(summary, expected, "format_slack_alerts_summary() formats notifications summary correctly")
