import datetime

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

from waste_notifier.models import Subscriber
from waste_schedule.models import ScheduleDetail


class SubscriberTests(TestCase):

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

    def test_invalid_data(self):

        INVALID_DATA = [
            { "phone_number": "234567891",  "waste_area_ids": "1,2,3", "service_type": "all" },
            { "phone_number": "2345678911", "waste_area_ids": "x", "service_type": "all" },
            { "phone_number": "2345678912", "waste_area_ids": "1,2,3", "service_type": "junk" },
        ]

        for data in INVALID_DATA:
            subscriber = Subscriber(**data)
            try:
                subscriber.clean()
            except ValidationError:
                self.assertRaisesMessage(ValidationError, '')
                continue

            # Throw an assertion if we ever get here
            self.fail("Data " + str(data) + " did not get validated")

    def test_subscribe_and_confirm(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code == 200, True)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
        self.assertEqual(response.status_code == 200, True)

    def test_subscribe_and_confirm(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='schedule', service_type='recycling', description='Unit Test Holiday', normal_day=datetime.date(2017, 4, 7), new_day=datetime.date(2017, 4, 8), note='')
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/')
        self.assertEqual(response.status_code == 200, True)

    def test_send_info(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1), note='')
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20180101/')
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.data['citywide'].get('5005550006'), "Phone number did not get alert")

    def test_send_no_info(self):
        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="8", service_type="all")
        subscriber.activate()
        detail = ScheduleDetail(detail_type='info', service_type='recycling', description='Special quarterly dropoff', normal_day=datetime.date(2018, 1, 1), note='')
        detail.save()

        c = Client()
        response = c.get('/waste_notifier/send/20180102/')
        self.assertTrue(response.status_code == 200)
        self.assertFalse(response.data['citywide'].get('5005550006'), "Phone number should not have gotten alert")
