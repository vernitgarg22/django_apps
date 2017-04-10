from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

from waste_notifier.models import Subscriber


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
            assert(false)

    def test_subscribe_and_confirm(self):

        c = Client()

        response = c.post('/waste_notifier/subscribe/', { "phone_number": "5005550006", "waste_area_ids": "2,3,14,", "service_type": "all" } )
        self.assertEqual(response.status_code == 200, True)

        response = c.post('/waste_notifier/confirm/', { "From": "5005550006", "Body": "ADD ME" } )
        self.assertEqual(response.status_code == 200, True)
