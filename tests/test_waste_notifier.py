import datetime

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

import cod_utils.util
import cod_utils.security
import tests.disabled

from waste_notifier.models import Subscriber
from waste_schedule.models import ScheduleDetail

import waste_notifier.views


def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(Subscriber)
    cleanup_model(ScheduleDetail)


def add_meta(content, date = cod_utils.util.tomorrow()):
    """
    Add meta data for the /send endpoint (e.g., date)
    """
    meta = {
        'meta': {
            'current_time': datetime.datetime.today().strftime("%Y-%m-%d %H:%M"),
            'date_applicable': date.strftime("%Y-%m-%d"),
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

    def test_subscriber_comment(self):
        """
        Test subscriber with comment
        """
        s = Subscriber(phone_number="1234567890", waste_area_ids="1", service_type="all")
        s.save()
        waste_notifier.views.add_subscriber_comment("1234567890", "testing")
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

        self.assertEqual(subscriber.status, 'inactive', "User's status should be inactive")
        self.assertEqual(subscriber.comment, "User's response to confirmation was: oops", "User's comment should contain their invalid response")

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
        self.assertEqual(date_applicable, '2017-04-21 00:00:00', "Alerts run with 'today' passed in should run a day later")

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