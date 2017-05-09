from datetime import datetime
from datetime import timedelta
from decimal import *
import pytz

from django.test import Client
from django.test import TestCase

from django.utils import timezone

import tests.disabled

from assessments import util
from assessments import views

from assessments.models import Sales, ParcelMaster


def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(Sales)
    cleanup_model(ParcelMaster)

def make_sale():
    data = {'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'saledate': datetime(2013, 6, 3, 0, 0), 'addresscombined': '7840 VAN DYKE PL', 'pnum': '17000074.001', 'terms': 'REVIEW NEEDED', 'instr': 'PTA', 'saleprice': Decimal('35000')}
    sale = Sales(**data)
    sale.save()
    return sale

def make_parcelmaster():
    data = {'resb_priceground': 29.04669, 'resb_occ': 0, 'cib_effage': 0, 'resb_depr': 38, 'propstreetcombined': '7840 VAN DYKE PL', 'cib_floorarea': 0.0, 'resb_value': 37325.0, 'cib_numcib': 0, 'resb_style': 'SINGLE FAMILY', 'cib_calcvalue': 0.0, 'cib_pricefloor': 0.0, 'resb_heat': 2, 'resb_calcvalue': 106948.421875, 'resb_nbed': 0, 'resb_exterior': 3, 'ownerstate': 'MI', 'ownercity': 'DETROIT', 'resb_pricefloor': 13.31134, 'resb_gartype': 1, 'resb_yearbuilt': 1914, 'resb_garagearea': 504, 'resb_groundarea': 1285, 'resb_fireplaces': 1, 'resb_styhgt': 5, 'resb_basementarea': 1110, 'resb_bldgclass': 2, 'cib_yearbuilt': 0, 'ownername2': '', 'relatedpnum': '', 'resb_avestyht': 2.1821, 'resb_plusminus': 0, 'cib_bldgclass': 0, 'pnum': '17000074.001', 'resb_effage': 52, 'resb_fullbaths': 2, 'resb_floorarea': 2804, 'cib_occ': 0, 'cibunits': 0, 'resb_halfbaths': 1, 'ownerstreetaddr': '7840 VAN DYKE PL', 'cibbedrooms': 0, 'ownerzip': '48214', 'ownername1': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'xstreetname_1': 'SEYBURN', 'xstreetname_0': 'VAN DYKE', 'resb_numresb': 1, 'cib_stories': 0, 'cib_value': 0.0}
    pm = ParcelMaster(**data)
    pm.save()
    return pm


class AssessmentsTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()
        self.maxDiff = None

    def test_clean_pnum(self):
        self.assertEqual(util.clean_pnum('1245.1234'), '1245.1234', "clean_pnum() replaces periods with underscores")

    def test_clean_parcel_val(self):
        self.assertEqual(util.clean_parcel_val(" foo "), "foo", "clean_parcel_val() strips trailing and leading white space")

    def test_get_parcel_descriptions(self):
        descriptions = util.get_parcel_descriptions()
        self.assertTrue(descriptions and type(descriptions) is dict)

    def test_sales_empty(self):
        sales = Sales.objects.all()
        self.assertTrue(len(sales) == 0)

    def test_sales(self):
        sale = make_sale()
        self.assertTrue(str(sale) != '')

    def test_sales_json(self):
        sale = make_sale()
        self.assertTrue(sale.json() != {})

    def test_parcelmaster(self):
        pm = make_parcelmaster()
        self.assertTrue(str(pm) != '')

    def test_parcelmaster_json(self):
        pm = make_parcelmaster()
        self.assertTrue(pm.json() != {})

    def test_get_sales(self):

        sale = make_sale()
        c = Client()

        response = c.get('/assessments/17000074_001/')
        self.assertEqual(response.status_code, 200, "/assessments/<pnum>/ succeeds")
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 5, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
        self.assertListEqual(expected, response.data, "/assessments/<pnum>/ returns sales parcel data")

    def test_get_sales_404(self):

        c = Client()
        response = c.get('/assessments/0000/')
        self.assertEqual(response.status_code, 404, "/assessments/<pnum>/ returns 404 when property not found")

    def test_get_sales_address_search(self):

        sale = make_sale()
        c = Client()

        response = c.get('/assessments/address/7840 VAN DYKE PL/')
        self.assertEqual(response.status_code, 200, "/assessments/<address>/ succeeds")
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 5, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
        self.assertListEqual(expected, response.data, "/assessments/<address>/ returns sales data search results")

    def test_get_sales_address_search_recent(self):

        sale = make_sale()
        c = Client()

        response = c.get('/assessments/address/7840 VAN DYKE PL/recent/')
        self.assertEqual(response.status_code, 200, "/assessments/<address>/recent/ succeeds")
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 5, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
        self.assertListEqual(expected, response.data, "/assessments/<address>/recent/ gets current sales data search results")

    def test_get_sales_address_search_recent_filters_old(self):

        sale = make_sale()
        sale.saledate = sale.saledate - timedelta(days = 10 * 365)
        sale.save()
        c = Client()

        response = c.get('/assessments/address/7840 VAN DYKE PL/recent/')
        self.assertEqual(response.status_code, 404, "/assessments/<address>/recent/ filters out old sales data search results")

    def test_get_sales_address_search_recent_filters_custom(self):

        sale = make_sale()
        sale.saledate = sale.saledate - timedelta(days = 3 * 365)
        sale.save()
        sale = make_sale()
        sale.saledate = sale.saledate + timedelta(days = 4 * 365)
        sale.save()
        c = Client()

        response = c.get('/assessments/address/7840 VAN DYKE PL/recent/years/2/')
        self.assertEqual(response.status_code, 200, "/assessments/<address>/recent/years/<years>/ succeeds")
        expected = [{'pnum': '17000074.001', 'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'terms': 'REVIEW NEEDED', 'instr': 'PTA', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2017, 6, 2, 5, 0, tzinfo=pytz.utc), 'saleprice': Decimal('35000'), 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY'}]
        self.assertListEqual(expected, response.data, "/assessments/<address>/recent/years/<years>/ filters out old sales data search results")

    def test_get_sales_address_404(self):

        c = Client()
        response = c.get('/assessments/address/invalid/')
        self.assertEqual(response.status_code, 404, "/assessments/address/<address>/ returns 404 when property not found")

    def test_get_sales_property_recent(self):

        sale = make_sale()
        sale.save()
        c = Client()

        response = c.get('/assessments/17000074_001/recent/')
        self.assertEqual(response.status_code, 200, "/assessments/<pnum>/recent/ succeeds")
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 5, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
        self.assertListEqual(expected, response.data, "/assessments/<pnum>/recent/ gets current sales")

    def test_get_sales_property_recent_filters_old(self):

        sale = make_sale()
        sale.saledate = datetime(2010, 1, 1)
        sale.save()
        c = Client()

        response = c.get('/assessments/17000074_001/recent/')
        self.assertEqual(response.status_code, 404, "/assessments/<pnum>/recent/ filters out out old sales")

    def test_get_sales_property_recent_filters_custom(self):

        sale = make_sale()
        sale.saledate = sale.saledate - timedelta(days=4 * 365)
        sale.save()
        c = Client()

        response = c.get('/assessments/17000074_001/recent/years/3/')
        self.assertEqual(response.status_code, 404, "/assessments/<pnum>/recent/years/<years>/ filters out out old sales")

    def test_get_parcel_property(self):

        pm = make_parcelmaster()
        c = Client()
    
        response = c.get('/assessments/parcel/17000074_001/')
        self.assertEqual(response.status_code, 200, "/parcel/<pnum>/ succeeds")
        expected = { 'resb_gartype': 1, 'resb_calcvalue': 106948.421875, 'cib_pricefloor': 0.0, 'resb_exterior': 3, 'resb_priceground': 29.04669, 'resb_fullbaths': 2, 'resb_depr': 38, 'resb_heat': 2, 'ownerstreetaddr': '7840 VAN DYKE PL', 'xstreetname_1': 'SEYBURN', 'cib_value': 0.0, 'cib_yearbuilt': 0, 'ownerstate': 'MI', 'cib_numcib': 0, 'resb_floorarea': 2804, 'resb_bldgclass': 2, 'ownerzip': '48214', 'cib_bldgclass': 0, 'resb_occ': 0, 'cibbedrooms': 0, 'ownername1': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'cib_effage': 0, 'resb_style': 'SINGLE FAMILY', 'resb_plusminus': 0, 'resb_pricefloor': 13.31134, 'resb_avestyht': 2.1821, 'ownercity': 'DETROIT', 'cibunits': 0, 'resb_halfbaths': 1, 'cib_calcvalue': 0.0, 'ownername2': '', 'resb_value': 37325.0, 'resb_garagearea': 504, 'cib_stories': 0, 'resb_numresb': 1, 'pnum': '17000074.001', 'relatedpnum': '', 'cib_floorarea': 0.0, 'field_descriptions': {'resb_gartype': 'garage type', 'resb_calcvalue': 'resb_calcvalue', 'cib_pricefloor': 'cib_pricefloor', 'resb_exterior': 'exterior', 'resb_priceground': 'resb_priceground', 'resb_fullbaths': 'full baths', 'resb_depr': 'resb_depr', 'resb_heat': 'resb_heat', 'cib_numcib': 'commercial buildings', 'xstreetname_1': 'cross street', 'cib_value': 'cib_value', 'cib_yearbuilt': 'year built', 'ownerstate': 'owner state', 'ownerstreetaddr': 'owner address', 'resb_floorarea': 'floor area', 'resb_bldgclass': 'residential buidling class', 'ownerzip': 'owner zip', 'cib_bldgclass': 'commercial building class', 'resb_occ': 'residential building occupant', 'cibbedrooms': 'cibbedrooms', 'ownername1': 'owner', 'resb_yearbuilt': 'residential year built', 'resb_style': 'residential building style', 'resb_plusminus': 'resb_plusminus', 'resb_pricefloor': 'resb_pricefloor', 'resb_avestyht': 'resb_avestyht', 'ownercity': 'owner city', 'cibunits': 'number of units', 'resb_halfbaths': 'half baths', 'cib_calcvalue': 'cib_calcvalue', 'ownername2': 'additional owner', 'resb_value': 'resb_value', 'resb_garagearea': 'garage area', 'cib_stories': 'number of stories', 'resb_numresb': 'residential buildings', 'pnum': 'parcel number', 'relatedpnum': 'related parcel', 'cib_floorarea': 'floor area', 'resb_effage': 'resb_effage', 'resb_fireplaces': 'number of fire places', 'resb_groundarea': 'ground area', 'resb_nbed': 'number of bedrooms', 'cib_effage': 'cib_effage', 'propstreetcombined': 'address', 'cib_occ': 'commercial occupant', 'resb_basementarea': 'basement area', 'xstreetname_0': 'cross street', 'resb_styhgt': 'residential height'}, 'resb_effage': 52, 'resb_fireplaces': 1, 'resb_groundarea': 1285, 'resb_nbed': 0, 'resb_yearbuilt': 1914, 'propstreetcombined': '7840 VAN DYKE PL', 'cib_occ': 0, 'resb_basementarea': 1110, 'xstreetname_0': 'VAN DYKE', 'resb_styhgt': 5 }
        self.assertDictEqual(expected, response.data, "/parcel/<pnum>/ returns data for a parcel of land")

    def test_get_parcel_property_404(self):

        c = Client()
        response = c.get('/assessments/parcel/0000/')
        self.assertEqual(response.status_code, 404, "/assessments/parcel/<pnum>/ returns 404 when property not found")
