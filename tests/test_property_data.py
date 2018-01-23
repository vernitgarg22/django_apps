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
                    city="Detroit", postal_code="48214", active_date=date(2018, 1, 1), parcel_id="123.")
        site.save()

        c = Client()
        response = c.get("/property_data/dte/active_connections/123./", secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, { "active": True }, "property_data dte active connections indicates parcel has power")

    def test_get_dte_active_connections_notsecure(self):

        c = Client()
        response = c.get("/property_data/dte/active_connections/123./")

        self.assertEqual(response.status_code, 403)

    def test_get_dte_active_connections_badclient(self):

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.get("/property_data/dte/active_connections/123./", secure=True)

        self.assertEqual(response.status_code, 403)

        settings.ALLOWED_HOSTS.append("127.0.0.1")

    def test_get_dte_active_connections_not_found(self):

        c = Client()
        response = c.get("/property_data/dte/active_connections/123./", secure=True)

        self.assertEqual(response.status_code, 404)
