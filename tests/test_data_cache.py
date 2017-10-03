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
        response = c.get("/data_cache/test/")

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 200)
        self.assertEqual(data_value.data, response.data['data'], "Cached data should get returned")

    def test_data_cache_existing_data(self):

        init_test_data()

        data_source = DataSource.objects.first()
        data_source.get()

        c = Client()
        response = c.get("/data_cache/test/")

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 200)
        self.assertEqual(data_value.data, response.data['data'], "Cached data should get returned")

    def test_hydrant_data(self):

        init_hydrants_data()

        c = Client()
        response = c.get("/data_cache/hydrants/")

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 200)
        self.assertEqual(data_value.data, response.data['data'], "Cached data should get returned")

    def test_data_cache_invalid_auth(self):

        init_test_data_invalid_auth()

        c = Client()
        response = c.get("/data_cache/test/")

        data_value = DataValue.objects.first()
        self.assertTrue(response.status_code == 503)

    def test_data_cache_invalid_source1(self):

        init_hydrants_data()

        # remove data source url's format so that it defaults to html
        data_source = DataSource.objects.first()
        data_source.url = "https://gisweb.glwater.org/arcgis/rest/services/Hydrants/dwsd_HydrantInspection_v2/MapServer/0"
        data_source.save()

        c = Client()
        response = c.get("/data_cache/hydrants/")
        self.assertTrue(response.status_code == 503)

    def test_data_cache_invalid_source2(self):

        init_hydrants_data()

        # remove data source url's format so that it defaults to html
        data_source = DataSource.objects.first()
        data_source.url = "http://invalid"
        data_source.save()

        c = Client()
        response = c.get("/data_cache/hydrants/")
        self.assertTrue(response.status_code == 503)

    def test_data_cache(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/invalid/")
        self.assertTrue(response.status_code == 404)

