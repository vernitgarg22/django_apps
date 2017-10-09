import datetime
import json
import requests

from django.test import Client
from django.test import TestCase
from django.conf import settings

from data_cache.models import DataCredential, DataSource, DataValue

from cod_utils import util


# TODO put this in a util.py file
def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(DataSource)

def init_hydrants_creds():

    secret_creds = settings.CREDENTIALS['HYDRANTS']
    credentials = DataCredential(username=secret_creds['USERNAME'], password=secret_creds['PASSWORD'], referer=secret_creds['REFERER'], url=secret_creds['URL'])
    credentials.save()
    return credentials

def init_test_data():

    url = "https://jsonplaceholder.typicode.com/posts?userId=1"
    DataSource(name='test', url=url).save()

def init_test_data_invalid_auth():

    credentials = DataCredential(username="invalid", password="invalid", referer="invalid", url="http://invalid")
    credentials.save()

    url = "http://jsonplaceholder.typicode.com/posts?userId=1"
    DataSource(name='test', url=url, credentials=credentials).save()

def init_hydrants_data():

    credentials = init_hydrants_creds()
    DataSource(name='hydrants', url="https://gisweb.glwater.org/arcgis/rest/services/Hydrants/dwsd_HydrantInspection_v2/MapServer/0?f=json", credentials=credentials).save()

def init_test_data_invalid_source():

    url = "https://invalid"
    DataSource(name='test', url=url).save()

class DataCacheTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_data_cache(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(data_value.data), response.data['data'], "Cached data should get returned")

    def test_data_cache_existing_data(self):

        init_test_data()

        data_source = DataSource.objects.first()
        data_source.get()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(data_value.data), response.data['data'], "Cached data should get returned")

    def test_hydrant_data(self):

        init_hydrants_data()

        c = Client()
        response = c.get("/data_cache/hydrants/", secure=True)

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(data_value.data), response.data['data'], "Cached data should get returned")

    def test_data_cache_static(self):

        init_test_data()

        data_source = DataSource.objects.first()
        data_source.url = None
        data_source.save()
        data_value = DataValue(data_source=data_source, data='{"foo": "bar"}', updated=util.get_local_time())
        data_value.save()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.data['data'], {'foo': 'bar'}, "Cached static data should get returned")

    def test_data_cache_static_no_data(self):

        init_test_data()

        data_source = DataSource.objects.first()
        data_source.url = None
        data_source.save()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.data['data'], {}, "Cached static empty data should get returned when data value is empty")

    def test_data_cache_invalid_auth(self):

        init_test_data_invalid_auth()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 503)

    def test_data_cache_invalid_source1(self):

        init_hydrants_data()

        # remove data source url's format so that it defaults to html
        data_source = DataSource.objects.first()
        data_source.url = "https://gisweb.glwater.org/arcgis/rest/services/Hydrants/dwsd_HydrantInspection_v2/MapServer/0"
        data_source.save()

        c = Client()
        response = c.get("/data_cache/hydrants/", secure=True)
        self.assertTrue(response.status_code == 503)

    def test_data_cache_invalid_source2(self):

        init_hydrants_data()

        # remove data source url's format so that it defaults to html
        data_source = DataSource.objects.first()
        data_source.url = "http://invalid"
        data_source.save()

        c = Client()
        response = c.get("/data_cache/hydrants/", secure=True)
        self.assertTrue(response.status_code == 503)

    def test_data_cache_404(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/invalid/", secure=True)
        self.assertTrue(response.status_code == 404)

    def test_data_cache_not_secure(self):

        c = Client()
        response = c.get("/data_cache/test/")
        self.assertTrue(response.status_code == 403)

    def test_data_cache_blocked_client(self):

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.get("/data_cache/test/")

        settings.ALLOWED_HOSTS.append("127.0.0.1")

        self.assertTrue(response.status_code == 403)
