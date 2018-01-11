import requests
from datetime import date

from django.test import Client
from django.test import TestCase
from django.conf import settings

from tests import test_util

from data_cache.models import DTEActiveGasSite


def cleanup_db():
    test_util.cleanup_model(DTEActiveGasSite)

class PropertyDataTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_get_dte_active_connections(self):

        site = DTEActiveGasSite(business_partner="partner", contract_account=1, installation_number=1,
                    contract_number=1, connection_object=1, premise=1, house_number=1, street="woodward",
                    full_street_address="1 woodward", secondary_code="code", secondary_value="value",
                    city="Detroit", postal_code="48214", active_date=date(2018, 1, 1))
        site.save()

        c = Client()
        response = c.get("/property_data/dte/active_connections/1/", secure=True)

        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.data, { "owner": "partner" }, "property_data dte active connections indicates parcel has power")
