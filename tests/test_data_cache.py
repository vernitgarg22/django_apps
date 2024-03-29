import datetime
import json
import requests

from django.test import Client
from django.test import TestCase
from django.conf import settings

from tests import test_util
from unittest import skip
from unittest.mock import patch

from data_cache.models import DataCredential, DataSource, DataValue, DataSet, DataDescriptor, DataCitySummary
from data_cache.views import SimpleJSONCache

from cod_utils import util, security


def cleanup_db():
    test_util.cleanup_model(DataValue)
    test_util.cleanup_model(DataSource)
    test_util.cleanup_model(DataCitySummary)
    test_util.cleanup_model(DataSet)

    SimpleJSONCache.clear_all()


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

@skip('old hydrant data no longer available')
def init_hydrants_data():

    data_set = DataSet(name='hydrants')
    data_set.save()

    credentials = init_creds(key="HYDRANTS")
    DataSource(data_set=data_set, name='hydrants', url="https://gisweb.glwater.org/arcgis/rest/services/Hydrants/dwsd_HydrantInspection_v2/MapServer/0?f=json", credentials=credentials).save()

def init_hydrants_data_new():

    data_set = DataSet(name='hydrants')
    data_set.save()

    credentials = init_creds(key="HYDRANTS_NEW")
    DataSource(data_set=data_set, name='hydrants', url="http://gis.detroitmi.gov/arcgis/rest/services/DFD/HydrantInspection/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=4236&gdbVersion=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=&resultOffset=&resultRecordCount=&f=json", credentials=credentials).save()

def init_gis_data():

    data_set = DataSet(name='bridging_neighborhoods')
    data_set.save()

    credentials = init_creds(key="GIS")
    url = 'https://foobar.com'
    DataSource(data_set=data_set, name='bridging_neighborhoods', url=url, credentials=credentials, data_parse_path="features", data_id_parse_path="attributes/FID").save()

def init_test_data_invalid_source():

    data_set = DataSet(name='test')
    data_set.save()

    url = "https://invalid"
    DataSource(data_set=data_set, name='test', url=url).save()

class MockedGISResponse():

    def __init__(self):

        self.ok = True
        self.status_code = 200
        self.text = "dummy_token"

    def json(self):
        return {
            "error": { "code": 200 },
            "features": [
                {
                    "attributes": {
                        "FID": 100
                    }
                }
            ]
        }


class DataCacheTests(TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        cleanup_db()

    def test_data_cache(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        data_value = DataValue.objects.first()
        self.assertEqual(response.status_code,  200)
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
        self.assertEqual(response.status_code,  200)
        self.assertEqual(json.loads(data_value.data), response.data['data'], "Cached data should get returned")

    @skip('old hydrant data no longer available')
    def test_hydrant_data(self):

        init_hydrants_data()

        c = Client()
        response = c.get("/data_cache/hydrants/", secure=True)

        data_value = DataValue.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(data_value.data), response.data['data'], "Cached data should get returned")

    def test_hydrant_data_new(self):

        init_hydrants_data_new()

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

        self.assertEqual(response.status_code, 200)
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
        self.assertTrue(len(response.data['data']), "Response should contain data")
        self.assertTrue(response.data['key'].startswith('url_cache_'))

    def test_data_cache_url_cache_persists(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)
        self.assertEqual(response.status_code, 201)
        key = response.data['key']

        response = c.get("/data_cache/url_cache/{}/".format(key), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['data']), "Response should contain data")

    def test_data_cache_url_cache_not_secure(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url })
        self.assertEqual(response.status_code, 403)

    @skip('Blocking clients by IP not permitted by firewall')
    def test_data_cache_url_cache_blocked_client(self):

        url = "https://jsonplaceholder.typicode.com/posts/1"

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)

        settings.ALLOWED_HOSTS.append("127.0.0.1")

        self.assertEqual(response.status_code, 403)

    def test_data_cache_url_cache_no_data(self):

        url = "https://httpbin.org/xml"

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)

        self.assertEqual(response.status_code, 404)

    def test_data_cache_url_cache_no_url(self):

        c = Client()
        response = c.post("/data_cache/url_cache/urls/", secure=True)

        self.assertEqual(response.status_code, 400)

    def test_data_cache_user(self):

        data = { "data": { "sample": "this is sample data" }, "key": "test_data" }

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data=json.dumps(data), secure=True, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data'], data['data'], "Response should contain data")
        self.assertEqual(response.data['key'], 'user_cache_test_data')

    def test_data_cache_user_update(self):

        data = { "data": { "sample": "this is sample data" }, "key": "test_data" }

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data=json.dumps(data), secure=True, content_type="application/json")

        data = { "data": { "sample": "this is new sample data" }, "key": "test_data" }

        response = c.post("/data_cache/user_cache/data/", data=json.dumps(data), secure=True, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data'], data['data'], "Response should contain data")
        self.assertEqual(response.data['key'], 'user_cache_test_data')

    def test_data_cache_user_persists(self):

        data = { "data": { "sample": "this is sample data" }, "key": "test_data" }

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data=json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        key = response.data['key']

        response = c.get("/data_cache/user_cache/{}/".format(key), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'], data['data'], "Response should contain data")

    def test_data_cache_user_persists_not_secure(self):

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data={}, secure=False, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_data_cache_user_persists_missing_data(self):

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data={}, secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_data_cache_user_persists_missing_key(self):

        data = { "data": { "sample": "this is sample data" } }

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data=json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @skip('Blocking clients by IP not permitted by firewall')
    def test_data_cache_user_persists_blocked_client(self):

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.post("/data_cache/user_cache/data/", data={}, secure=True, content_type="application/json")

        settings.ALLOWED_HOSTS.append("127.0.0.1")

        self.assertEqual(response.status_code, 403)

    def test_data_cache_invalid_auth(self):

        init_test_data_invalid_auth()

        c = Client()
        response = c.get("/data_cache/test/", secure=True)

        data_value = DataValue.objects.first()
        self.assertEqual(response.status_code, 503)

    def test_data_cache_invalid_source1(self):

        init_hydrants_data()

        # remove data source url's format so that it defaults to html
        data_source = DataSource.objects.first()
        data_source.url = "https://gisweb.glwater.org/arcgis/rest/services/Hydrants/dwsd_HydrantInspection_v2/MapServer/0"
        data_source.save()

        c = Client()
        response = c.get("/data_cache/hydrants/", secure=True)
        self.assertEqual(response.status_code, 503)

    def test_data_cache_invalid_source2(self):

        init_hydrants_data()

        # remove data source url's format so that it defaults to html
        data_source = DataSource.objects.first()
        data_source.url = "http://invalid"
        data_source.save()

        c = Client()
        response = c.get("/data_cache/hydrants/", secure=True)
        self.assertEqual(response.status_code, 503)

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
        self.assertEqual(response.status_code, 404)

    def test_data_cache_param_404(self):

        init_test_data()

        c = Client()
        response = c.get("/data_cache/test/invalid/", secure=True)
        self.assertEqual(response.status_code, 404)

    def test_data_cache_not_secure(self):

        c = Client()
        response = c.get("/data_cache/test/")
        self.assertEqual(response.status_code, 403)

    def test_data_cache_params(self):

        init_gis_data()

        with patch.object(requests, 'post', return_value=MockedGISResponse()), patch.object(requests, 'get', return_value=MockedGISResponse()):

            c = Client()
            response = c.get("/data_cache/bridging_neighborhoods/100/", secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['attributes']['FID'], 100, "Data cache can be queried with a parameter")

    def test_data_cache_params_remove_orphans(self):

        init_gis_data()

        data_source = DataSource.objects.first()
        with patch.object(requests, 'post', return_value=MockedGISResponse()), patch.object(requests, 'get', return_value=MockedGISResponse()):
            data_source.refresh()

        self.assertEqual(DataValue.objects.count(), 1)

        data_value = DataValue(data_source=data_source, data='{"foo": "bar"}', param="orphan")
        data_value.save()
        self.assertEqual(DataValue.objects.get(param="orphan").id, data_value.id)

        with patch.object(requests, 'post', return_value=MockedGISResponse()), patch.object(requests, 'get', return_value=MockedGISResponse()):

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
        self.assertEqual(response.status_code, 503)

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


class DataCacheSecurityTests(TestCase):

    def setUp(self):
        init_test_data()
        self.maxDiff = None

    def tearDown(self):
        cleanup_db()

    def test_data_cache_get_data_blocked_client(self):

        "Retrieving data can be blocked by ip"

        with patch.object(security, 'block_client', return_value=True):

            c = Client()
            response = c.get("/data_cache/test/", secure=True)

        self.assertEqual(response.status_code, 403)

    def test_data_cache_add_url_blocked_client(self):

        "Adding url can be blocked by ip"

        url = "https://jsonplaceholder.typicode.com/posts/1"
        with patch.object(security, 'block_client', return_value=True):

            c = Client()
            response = c.post("/data_cache/url_cache/urls/", data={ "url": url }, secure=True)

        self.assertEqual(response.status_code, 403)

    def test_data_cache_add_user_cache_blocked_client(self):

        "Adding user cache can be blocked by ip"

        data = { "data": { "sample": "this is sample data" }, "key": "test_data" }
        with patch.object(security, 'block_client', return_value=True):

            c = Client()
            response = c.post("/data_cache/user_cache/data/", data=json.dumps(data), secure=True, content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_data_cache_refresh_cache_blocked_client(self):

        "Refreshing cache can be blocked by ip"

        with patch.object(security, 'block_client', return_value=True):

            c = Client()
            response = c.post("/data_cache/refresh/", secure=True)

        self.assertEqual(response.status_code, 403)

    def test_get_city_data_summaries_blocked_client(self):

        "Retrieving city data summaries can be blocked by ip"

        with patch.object(security, 'block_client', return_value=True):

            c = Client()
            response = c.get("/data_cache/city_data_summaries/")

        self.assertEqual(response.status_code, 403)


class DataCitySummaryTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def tearDown(self):
        cleanup_db()

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected, "City data summaries contains info about city overview datasets")

    def test_get_city_data_summaries_not_secure(self):

        c = Client()
        response = c.get("/data_cache/city_data_summaries/")
        self.assertEqual(response.status_code, 403)


class DataCacheRefreshTests(TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        cleanup_db()

    def test_refresh(self):

        init_test_data()

        c = Client()
        response = c.post("/data_cache/refresh/", secure=True)
        self.assertEqual(response.status_code, 201)

    def test_refresh_not_secure(self):

        c = Client()
        response = c.post("/data_cache/refresh/")
        self.assertEqual(response.status_code, 403)

    def test_refresh_blocked_client(self):

        # Force block_client to block us
        settings.ALLOWED_HOSTS.remove("127.0.0.1")

        c = Client()
        response = c.post("/data_cache/refresh/")

        settings.ALLOWED_HOSTS.append("127.0.0.1")

        self.assertEqual(response.status_code, 403)
