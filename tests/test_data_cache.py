import datetime
import json
import requests

from django.test import Client
from django.test import TestCase
from django.conf import settings

from tests import test_util

from data_cache.models import DataCredential, DataSource, DataValue, DataSet, DataDescriptor, DataCitySummary

from cod_utils import util


def cleanup_db():
    test_util.cleanup_model(DataSource)
    test_util.cleanup_model(DataSet)
    test_util.cleanup_model(DataCitySummary)

def init_creds(key):

    secret_creds = settings.CREDENTIALS[key]
    credentials = DataCredential(username=secret_creds['USERNAME'], password=secret_creds['PASSWORD'], referer=secret_creds['REFERER'], url=secret_creds['URL'])
    credentials.save()
    return credentials

def init_test_data(url="https://jsonplaceholder.typicode.com/posts?userId=1"):

    data_set = DataSet.objects.get_or_create(name='test')
    name="test{}".format(DataSource.objects.count())
    DataSource(data_set=data_set[0], name=name, url=url).save()

def init_test_data_invalid_auth():

    data_set = DataSet(name="test")
    data_set.save()

    credentials = DataCredential(username="invalid", password="invalid", referer="invalid", url="http://invalid")
    credentials.save()

    url = "http://jsonplaceholder.typicode.com/posts?userId=1"
    DataSource(data_set=data_set, name='test', url=url, credentials=credentials).save()

def init_hydrants_data():

    data_set = DataSet(name='hydrants')
    data_set.save()

    credentials = init_creds(key="HYDRANTS")
    DataSource(data_set=data_set, name='hydrants', url="https://gisweb.glwater.org/arcgis/rest/services/Hydrants/dwsd_HydrantInspection_v2/MapServer/0?f=json", credentials=credentials).save()

def init_gis_data():

    data_set = DataSet(name='bridging_neighborhoods')
    data_set.save()

    credentials = init_creds(key="GIS")
    url = 'https://gis.detroitmi.gov/arcgis/rest/services/DoIT/bridging_neighborhoods/MapServer/0/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=FID%2C+parcelno%2C+programare&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=json'
    DataSource(data_set=data_set, name='bridging_neighborhoods', url=url, credentials=credentials, data_parse_path="features", data_id_parse_path="attributes/FID").save()

def init_test_data_invalid_source():

    data_set = DataSet(name='test')
    data_set.save()

    url = "https://invalid"
    DataSource(data_set=data_set, name='test', url=url).save()

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

    def test_data_cache_refresh(self):

        init_test_data()

        data_source = DataSource.objects.first()
        data_source.refresh()
        data_value = DataValue.objects.first()
        data_source.refresh()
        self.assertEqual(data_value.id, DataValue.objects.first().id, "Cached data can be refreshed")

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
        self.assertEqual(response.status_code, 200)
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

        self.assertEqual(response.status_code, 503)

    def test_data_cache_multiple_sources_per_set(self):

        init_test_data()
        init_test_data("https://jsonplaceholder.typicode.com/posts?userId=2")
        # DataSource(data_set=DataSet.objects.first(), name='test2', url=url).save()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 20, "Multiple data sources per data set can get returned")

    def test_data_cache_multiple_dict_sources_per_set(self):

        init_test_data(url="https://jsonplaceholder.typicode.com/posts/1")
        init_test_data(url="https://jsonplaceholder.typicode.com/posts/2")

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 4, "Multiple data dict sources per data set can get returned")

    def test_data_cache_url_cache(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['data']), 4, "Response should contain data")
        self.assertTrue(response.data['key'].startswith('url_cache_'))

    def test_data_cache_url_cache_persists(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)
        self.assertEqual(response.status_code, 201)
        key = response.data['key']

        response = c.get("/data_cache/url_cache/{}/".format(key), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 4, "Response should contain data")

    def test_data_cache_url_cache_not_secure(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url })
        self.assertEqual(response.status_code, 403)

    def test_data_cache_url_cache_blocked_client(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)

        settings.ALLOWED_HOSTS.append("127.0.0.1")

        self.assertTrue(response.status_code == 403)

    def test_data_cache_url_cache_no_data(self):

        url = "https://httpbin.org/xml"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)

        self.assertEqual(response.status_code, 404)

    def test_data_cache_url_cache_no_url(self):

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", secure=True)

        self.assertEqual(response.status_code, 400)

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

    def test_data_cache_value_rejects_bad_json(self):

        init_test_data()

        data_value = DataValue(data_source=DataSource.objects.first(), data='invalid')
        with self.assertRaises(Exception, msg="DataValue.save() should reject invalid json") as error:
            data_value.save()

        del data_value

    def test_data_cache_404(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/invalid/", secure=True)
        self.assertTrue(response.status_code == 404)

    def test_data_cache_param_404(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/test/invalid/", secure=True)
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

    def test_data_cache_params(self):

        init_gis_data()

        c = Client()
        response = c.get("/data_cache/bridging_neighborhoods/100/", secure=True)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.json()['data']['attributes']['FID'], 100, "Data cache can be queried with a parameter")

    def test_data_cache_params_remove_orphans(self):

        init_gis_data()

        data_source = DataSource.objects.first()
        data_source.refresh()
        self.assertEqual(DataValue.objects.count(), 101)

        data_value = DataValue(data_source=data_source, data='{"foo": "bar"}', param="orphan")
        data_value.save()
        self.assertEqual(DataValue.objects.get(param="orphan").id, data_value.id)

        # DataSource.refresh() should remove the orphan DataValue object
        data_source.refresh()

        self.assertTrue(DataValue.objects.filter(param="orphan").count() == 0)

    def test_receiving_bad_json(self):

        init_test_data()

        data_source = DataSource.objects.first()
        data_source.url = "https://httpbin.org/xml"
        data_source.save(0)

        c = Client()
        response = c.get("/data_cache/test/", secure=True)
        self.assertTrue(response.status_code == 503)

    def test_socrata_where_clause(self):

        url ="https://data.detroitmi.gov/resource/uzpg-2pfj.json"
        socrata_where="demolition_date > '1_week_back'"
        data_source = DataSource(name="demolitions", url=url, socrata_where=socrata_where)
        data_source.save()

        data_value = data_source.get()

        self.assertTrue(data_value.data)

    def test_socrata_where_clause_invalid(self):

        url ="https://data.detroitmi.gov/resource/uzpg-2pfj.json"
        socrata_where="demolition_date junk '1_week_back'"
        data_source = DataSource(name="demolitions", url=url, socrata_where=socrata_where)
        data_source.save()

        with self.assertRaises(Exception, msg="DataSource.get() should flag failed get") as error:
            data_value = data_source.get()


class DataCitySummaryTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_get_city_data_summaries(self):

        init_test_data()

        descriptor = DataDescriptor(descriptor_type="department", value="DPW")
        descriptor.save()

        DataCitySummary(name="test", url="https://apis.detroitmi.gov/data_cache/test/", descriptor=descriptor).save()
        DataCitySummary(name="test_data_set", data_set=DataSet.objects.first()).save()

        expected = {
            "terms": {
                "department":  [ "DPW" ]
            },
            "summaries": [
                {
                    'name': 'test',
                    'description': '',
                    'data_set': None,
                    'url': 'https://apis.detroitmi.gov/data_cache/test/',
                    'credentials': None,
                    "terms": [
                        {
                            "type": "department",
                            "value": "DPW"
                        }
                    ]
                },
                {
                    'name': 'test_data_set',
                    'description': '',
                    'data_set': 'test',
                    'url': 'https://testserver/data_cache/test/',
                    'credentials': None,
                    "terms": [{}]
                }
            ]
        }

        c = Client()
        response = c.get("/data_cache/city_data_summaries/", secure=True)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.data, expected, "City data summaries contains info about city overview datasets")

    def test_get_city_data_summaries_not_secure(self):

        c = Client()
        response = c.get("/data_cache/city_data_summaries/")
        self.assertEqual(response.status_code, 403)