import datetime

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

from waste_notifier.models import Subscriber
from waste_schedule.models import ScheduleDetail


class WasteNotifierTests(TestCase):

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

    def test_subscribe_and_confirm(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code == 200, True)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
        self.assertEqual(response.status_code == 200, True)

        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.status == 'active', True)
        self.assertEqual(subscriber.last_status_update != None and subscriber.last_status_update != '', True)

    def test_subscribe_and_decline(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code == 200, True)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "REMOVE ME" } )
        self.assertEqual(response.status_code == 200, True)

        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.status == 'inactive', True)
        self.assertEqual(subscriber.last_status_update != None and subscriber.last_status_update != '', True)

    def test_send_reminder(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="0", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.get('/waste_notifier/send/20170417/')
        self.assertTrue(response.status_code == 200)
        expected = {'trash': {0: {'5005550006': 1}, 1: {}, 14: {}}, 'recycling': {1: {}, 22: {}}, 'bulk': {1: {}, 10: {}}, 'citywide': {}}
        self.assertDictEqual(expected, response.data, "Phone number did not get reminder")

    def test_send_info(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20180101/')
        self.assertTrue(response.status_code == 200)
        expected = {'recycling': {1: {}, 22: {}}, 'bulk': {1: {}, 10: {}}, 'citywide': {'5005550006': 1}, 'trash': {0: {}, 1: {}, 14: {}}}
        self.assertDictEqual(expected, response.data, "Phone number did not get info")

    def test_send_no_info(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1))
        detail.clean()
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20180102/')
        self.assertTrue(response.status_code == 200)
        expected = {'trash': {2: {}, 3: {}, 13: {}}, 'bulk': {2: {}, 12: {}}, 'recycling': {2: {}, 19: {}, 20: {}}, 'citywide': {}}
        self.assertDictEqual(expected, response.data, "Phone number should not have gotten info")

    def test_send_schedule_change(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20170407/')
        self.assertTrue(response.status_code == 200)
        expected = {'bulk': {8: {'5005550006': 1}, 19: {}}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'citywide': {}, 'recycling': {8: {'5005550006': 1}, 11: {}}}
        self.assertDictEqual(expected, response.data, "Phone number should have gotten recycling reschedule alert")

    def test_send_no_schedule_change(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='test holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8))
        detail.clean()
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20170408/')
        self.assertTrue(response.status_code == 200)
        expected = {'citywide': {}}
        self.assertDictEqual(expected, response.data, "Phone number not should have gotten alert")

    def test_send_ab_onweek(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.get('/waste_notifier/send/20170407/')
        self.assertTrue(response.status_code == 200)
        expected = {'recycling': {8: {'5005550006': 1}, 11: {}}, 'citywide': {}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'bulk': {8: {'5005550006': 1}, 19: {}}}
        self.assertDictEqual(expected, response.data, "Alerts for a/b onweek failed")

    def test_send_ab_offweek(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()

        c = Client()
        response = c.get('/waste_notifier/send/20170414/')
        self.assertTrue(response.status_code == 200)
        expected = {'recycling': {9: {}, 10: {}}, 'bulk': {9: {}, 18: {}}, 'citywide': {}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}}
        self.assertDictEqual(expected, response.data, "Alerts for a/b offweek failed")

    def test_send_mix_days(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="12,14,22", service_type="all")
        subscriber.activate()

        c = Client()
        date_results = {
            '20170417': {'recycling': {1: {}, 22: {'5005550006': 1}}, 'citywide': {}, 'trash': {0: {}, 1: {}, 14: {'5005550006': 1}}, 'bulk': {1: {}, 10: {}}},
            '20170418': {'trash': {2: {}, 3: {}, 13: {}}, 'citywide': {}, 'recycling': {2: {}, 19: {}, 20: {}}, 'bulk': {2: {}, 12: {'5005550006': 1}}},
            '20170419': {'bulk': {4: {}, 15: {}}, 'recycling': {16: {}, 17: {}, 4: {}}, 'trash': {11: {}, 4: {}, 5: {}}, 'citywide': {}}
        }

        for date, expected in date_results.items():
            response = c.get("/waste_notifier/send/{}/".format(date))
            self.assertTrue(response.status_code == 200)
            self.assertDictEqual(expected, response.data, "Alerts for subscriber with mix of pickup days failed")

    def test_send_start_date(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='start-date', service_type='yard waste', description='Citywide yard waste pickup starts monday, April 17, 2017', new_day=datetime.date(2017, 4, 17))
        detail.clean()
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20170417/')
        self.assertTrue(response.status_code == 200)
        expected = {'trash': {0: {}, 1: {}, 14: {}}, 'citywide': {'5005550006': 1}, 'recycling': {1: {}, 22: {}}, 'bulk': {1: {}, 10: {}}}
        self.assertDictEqual(expected, response.data, "Yard waste start date alert should have been sent")

    def test_send_end_date(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='end-date', service_type='yard waste', description='Citywide yard waste pickup ends friday, December 15, 2017', new_day=datetime.date(2017, 12, 15))
        detail.clean()
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20171215/')
        self.assertTrue(response.status_code == 200)
        expected = {'recycling': {8: {'5005550006': 1}, 11: {}}, 'bulk': {8: {'5005550006': 1}, 19: {}}, 'trash': {8: {'5005550006': 1}, 9: {}, 10: {}}, 'citywide': {'5005550006': 1}}
        self.assertDictEqual(expected, response.data, "Yard waste end date alert should have been sent")
