import datetime

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

import cod_utils.util
import cod_utils.security
import tests.disabled

from waste_notifier.models import Subscriber
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
        detail.save()
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save()

        services = views.add_additional_services(['bulk'], datetime.date(2017, 7, 1))
        self.assertListEqual(['bulk', 'yard waste'], services, "Yard waste, when active and bulk is getting picked up, gets added to list of services")

    def test_get_service_message(self):
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save()
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save()

        message = views.get_service_message(['bulk'], datetime.date(2017, 7, 1))
        self.assertEqual(message, 'City of Detroit Public Works:  Your next pickup for bulk and yard waste is Jul 01, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).')

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
        response = c.post('/waste_notifier/send/20170417/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'trash': {0: {'5005550006': 1}, 1: {}, 14: {}}, 'recycling': {1: {}, 27: {}}, 'bulk': {1: {}, 29: {}}, 'citywide': {}}, date=datetime.date(2017, 4, 17))
        self.assertDictEqual(expected, response.data, "Phone number did not get reminder")

    def test_send_info(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/20180101/')
        self.assertEqual(response.status_code, 200)
        expected = {'recycling': {1: {}, 27: {}}, 'bulk': {1: {}, 29: {}}, 'citywide': {'5005550006': 1}, 'trash': {0: {}, 1: {}, 14: {}}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 1))
        self.assertDictEqual(expected, response.data, "Phone number did not get info")

    def test_send_no_info(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/20180102/')
        self.assertEqual(response.status_code, 200)
        expected = {'trash': {2: {}, 3: {}, 13: {}}, 'bulk': {2: {}, 31: {}}, 'recycling': {2: {}, 24: {}, 25: {}}, 'citywide': {}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 2))
        self.assertDictEqual(expected, response.data, "Phone number should not have gotten info")

    def test_send_info_all_services(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='all', description='City services have not affected by snow storm', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/20180101/')
        self.assertEqual(response.status_code, 200)
        expected = {'trash': {0: {}, 1: {}, 14: {}}, 'recycling': {1: {}, 27: {}}, 'meta': {'current_time': '2017-05-01 14:09', 'dry_run': True, 'date_applicable': '2018-01-01'}, 'citywide': {'5005550006': 1}, 'bulk': {1: {}, 29: {}}}
        expected = add_meta(expected, date = datetime.date(2018, 1, 1))
        self.assertDictEqual(expected, response.data, "Phone number did not get info")

    def test_send_schedule_change(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/20170407/')
        self.assertEqual(response.status_code, 200)
        expected = {'bulk': {38: {}}, 'citywide': {}, 'recycling': {16: {}}}
        expected = add_meta(expected, date = datetime.date(2017, 4, 7))
        self.assertDictEqual(expected, response.data, "Phone number should have gotten recycling reschedule alert")

    def test_send_no_schedule_change(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save()

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
        expected = add_meta({'recycling': {8: {'5005550006': 1}, 16: {}}, 'citywide': {}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'bulk': {8: {'5005550006': 1}, 38: {}}}, date=datetime.date(2017, 4, 7))
        self.assertDictEqual(expected, response.data, "Alerts for a/b onweek failed")

    def test_send_ab_offweek(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170414/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'recycling': {9: {}, 15: {}}, 'bulk': {9: {}, 37: {}}, 'citywide': {}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}}, date=datetime.date(2017, 4, 14))
        self.assertDictEqual(expected, response.data, "Alerts for a/b offweek failed")

    def test_send_mix_days(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="12,14,22", service_type="all")
        subscriber.activate()

        c = Client()
        date_results = {
            '20170417': {'recycling': {1: {}, 27: {}}, 'citywide': {}, 'trash': {0: {}, 1: {}, 14: {'5005550006': 1}}, 'bulk': {1: {}, 29: {}}},
            '20170418': {'trash': {2: {}, 3: {}, 13: {}}, 'citywide': {}, 'recycling': {2: {}, 24: {}, 25: {}}, 'bulk': {2: {}, 31: {}}},
            '20170419': {'bulk': {4: {}, 34: {}}, 'recycling': {4: {}, 21: {}, 22: {'5005550006': 1}}, 'trash': {11: {}, 4: {}, 5: {}}, 'citywide': {}}
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
        expected = add_meta({'bulk': {34: {}, 4: {}}, 'recycling': {4: {}, 21: {}, 22: {}}, 'trash': {11: {'5005550006': 1}, 4: {}, 5: {}}, 'citywide': {}}, date=datetime.date(2017, 4, 19))
        self.assertDictEqual(expected, response.data, "Eastside wednesday trash residents should have gotten alerts")

    def test_send_eastside_thursday_bulk_a(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="11,28,35", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170420/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'recycling': {17: {}, 18: {}, 7: {}}, 'citywide': {}, 'trash': {12: {}, 6: {}, 7: {}}, 'bulk': {35: {'5005550006': 1}, 7: {}}}, date=datetime.date(2017, 4, 20))
        self.assertDictEqual(expected, response.data, "Eastside thursday bulk A residents should have gotten alerts")

    def test_send_eastside_thursday_recycling_b(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="11,28,35", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.post('/waste_notifier/send/20170413/')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'recycling': {28: {'5005550006': 1}, 6: {}}, 'citywide': {}, 'trash': {12: {}, 6: {}, 7: {}}, 'bulk': {36: {}, 6: {}}}, date=datetime.date(2017, 4, 13))
        self.assertDictEqual(expected, response.data, "Eastside thursday recycling B residents should have gotten alerts")

    def test_send_bulk_yard_waste(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts', new_day=datetime.date(2017, 3, 1))
        detail.clean()
        detail.save()
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends', new_day=datetime.date(2017, 12, 1))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/?today=20170504')
        self.assertEqual(response.status_code, 200)
        expected = add_meta({'recycling': {8: {'5005550006': 1}, 16: {}}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'bulk': {8: {'5005550006': 1}, 38: {}}, 'citywide': {}}, date=datetime.date(2017, 5, 5))
        self.assertDictEqual(expected, response.data, "Yard waste alerts get included whenever bulk pickup happens and yard waste pickup is active")

    def test_send_start_date(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts monday, April 17, 2017', new_day=datetime.date(2017, 4, 17))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/20170417/')
        self.assertEqual(response.status_code, 200)
        expected = {'trash': {0: {}, 1: {}, 14: {}}, 'citywide': {'5005550006': 1}, 'recycling': {1: {}, 27: {}}, 'bulk': {1: {}, 29: {}}}
        expected = add_meta(expected, date=datetime.date(2017, 4, 17))
        self.assertDictEqual(expected, response.data, "Yard waste start date alert should have been sent")

    def test_send_end_date(self):

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends friday, December 15, 2017', new_day=datetime.date(2017, 12, 15))
        detail.clean()
        detail.save()

        c = Client()
        response = c.post('/waste_notifier/send/20171215/')
        self.assertEqual(response.status_code, 200)
        expected = {'recycling': {8: {'5005550006': 1}, 16: {}}, 'bulk': {8: {'5005550006': 1}, 38: {}}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'citywide': {'5005550006': 1}}
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
        week_routes = ScheduleDetailMgr.instance().get_regular_week_routes()
        expected = [{0: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 1: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 30: {'contractor': 'advance', 'week': 'b', 'services': 'bulk'}, 26: {'contractor': 'advance', 'week': 'b', 'services': 'recycle'}, 27: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 29: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 14: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}}, {32: {'contractor': 'advance', 'week': 'b', 'services': 'bulk'}, 2: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 3: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 23: {'contractor': 'advance', 'week': 'b', 'services': 'recycle'}, 24: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 25: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 13: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 31: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}}, {33: {'contractor': 'advance', 'week': 'b', 'services': 'bulk'}, 34: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 19: {'contractor': 'advance', 'week': 'b', 'services': 'recycle'}, 20: {'contractor': 'advance', 'week': 'b', 'services': 'recycle'}, 5: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 22: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 4: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 11: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 21: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}}, {17: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 18: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 35: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 36: {'contractor': 'advance', 'week': 'b', 'services': 'bulk'}, 6: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 7: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 28: {'contractor': 'advance', 'week': 'b', 'services': 'recycle'}, 12: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}}, {16: {'contractor': 'advance', 'week': 'a', 'services': 'recycle'}, 37: {'contractor': 'advance', 'week': 'b', 'services': 'bulk'}, 38: {'contractor': 'advance', 'week': 'a', 'services': 'bulk'}, 8: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 9: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}, 10: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}, 15: {'contractor': 'advance', 'week': 'b', 'services': 'recycle'}}, {}, {}]
        self.assertEqual(week_routes, expected, "get_regular_week_routes() returns array of routes for a week")

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
        expected = [{0: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 1: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 30: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 26: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 27: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 29: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 14: {'services': 'trash', 'contractor': 'advance', 'week': ' '}}, {32: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 2: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 3: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 23: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 24: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 25: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 13: {'services': 'trash', 'contractor': 'advance', 'week': ' '}, 31: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}}, {33: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 34: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 19: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 20: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 5: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 22: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 4: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 11: {'services': 'trash', 'contractor': 'advance', 'week': ' '}, 21: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}}, {17: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 18: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 35: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 36: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 6: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 7: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 28: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 12: {'services': 'trash', 'contractor': 'advance', 'week': ' '}}, {16: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 37: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 38: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 8: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 9: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 10: {'services': 'trash', 'contractor': 'advance', 'week': ' '}, 15: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}}, {}, {}]
        self.assertEqual(week_routes, expected, "get_week_routes() returns array of routes for a week")

    def test_get_week_routes_holiday(self):
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        week_routes = ScheduleDetailMgr.instance().get_week_routes(date = datetime.date(2017, 5, 5))
        expected = [{}, {0: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 1: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 30: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 26: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 27: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 29: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 14: {'services': 'trash', 'contractor': 'advance', 'week': ' '}}, {32: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 2: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 3: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 23: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 24: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 25: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 13: {'services': 'trash', 'contractor': 'advance', 'week': ' '}, 31: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}}, {33: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 34: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 19: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 20: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 5: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 22: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 4: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 11: {'services': 'trash', 'contractor': 'advance', 'week': ' '}, 21: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}}, {17: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 18: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 35: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 36: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 6: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 7: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 28: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}, 12: {'services': 'trash', 'contractor': 'advance', 'week': ' '}}, {16: {'services': 'recycle', 'contractor': 'advance', 'week': 'a'}, 37: {'services': 'bulk', 'contractor': 'advance', 'week': 'b'}, 38: {'services': 'bulk', 'contractor': 'advance', 'week': 'a'}, 8: {'services': 'all', 'contractor': 'gfl', 'week': 'a'}, 9: {'services': 'all', 'contractor': 'gfl', 'week': 'b'}, 10: {'services': 'trash', 'contractor': 'advance', 'week': ' '}, 15: {'services': 'recycle', 'contractor': 'advance', 'week': 'b'}}, {}]
        self.assertEqual(week_routes, expected, "get_week_routes() reschdules array of routes for a week around holidays")

    def test_get_day_routes(self):
        routes = ScheduleDetailMgr.instance().get_day_routes(date = datetime.date(2017, 5, 5))
        expected = { 16: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 37: {'contractor': 'advance', 'services': 'bulk', 'week': 'b'}, 38: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 8: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 9: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 10: {'contractor': 'advance', 'services': 'trash', 'week': ' '}, 15: {'contractor': 'advance', 'services': 'recycle', 'week': 'b'} }
        self.assertEqual(routes, expected, "get_day_routes() returns routes for a date")

    def test_get_day_routes_holiday(self):
        detail = ScheduleDetail(detail_type='schedule', service_type='all', description='test holiday', normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        detail.clean()
        detail.save(null_waste_area_ids=True)
        routes = ScheduleDetailMgr.instance().get_day_routes(date = datetime.date(2017, 5, 5))
        expected = {17: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 18: {'contractor': 'advance', 'services': 'recycle', 'week': 'a'}, 35: {'contractor': 'advance', 'services': 'bulk', 'week': 'a'}, 36: {'contractor': 'advance', 'services': 'bulk', 'week': 'b'}, 6: {'contractor': 'gfl', 'services': 'all', 'week': 'b'}, 7: {'contractor': 'gfl', 'services': 'all', 'week': 'a'}, 28: {'contractor': 'advance', 'services': 'recycle', 'week': 'b'}, 12: {'contractor': 'advance', 'services': 'trash', 'week': ' '}}
        self.assertEqual(routes, expected, "get_day_routes() reschedules routes for a date if there is a holiday earlier in the week")

