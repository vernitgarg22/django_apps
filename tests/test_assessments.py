import os
from datetime import datetime
from datetime import timedelta
from decimal import *
import pytz

from django.conf import settings

from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone

from django.test import Client
from django.test import TestCase

import mock

import tests.disabled
from tests import test_util
from unittest import skip

from assessments import util
from assessments import views

from assessments.models import Sales, ParcelMaster
from assessments.models import Parcel, RoleType, CaseType, CaseMain, Sketch
from assessments.models import BSAPARCELDATA


def cleanup_db():
    test_util.cleanup_model(ParcelMaster)
    test_util.cleanup_model(Sales)
    test_util.cleanup_model(CaseMain)
    test_util.cleanup_model(CaseType)
    test_util.cleanup_model(RoleType)
    test_util.cleanup_model(Parcel)
    test_util.cleanup_model(Sketch)
    test_util.cleanup_model(BSAPARCELDATA)


def make_sale():
    data = {'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'saledate': datetime(2013, 6, 3, 0, 0, tzinfo=pytz.utc), 'addresscombined': '7840 VAN DYKE PL', 'pnum': '17000074.001', 'terms': 'REVIEW NEEDED', 'instr': 'PTA', 'saleprice': Decimal('35000')}
    sale = Sales(**data)
    sale.save()
    return sale

bsaparceldata = [ 
    {
        'PARCELNO': '17000074.001', 'DISTRICT': 3, 'COUNCIL': '05', 'ECF': '3142A', 'PROPADDR': '7840 VAN DYKE PL', 'PROPNO': 7840.0, 'PROPDIR': '', 'PROPSTR': 'VAN DYKE PL', 'ZIPCODE': '48214', 'TAXPAYER1': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'TAXPAYER2': '', 'TAXPADDR': '7840 VAN DYKE PL', 'TAXPCITY': 'DETROIT', 'TAXPSTATE': 'MI', 'TAXPZIP': '48214', 'propclass': '401', 'PROPCLASS1': '401', 'TAXSTATUS': 'TAXABLE', 'TAXSTATUS1': 'TAXABLE', 'zoning': 'R2', 'TOTALSQFT': 8948.0, 'TOTALACREAGE': 0.205, 'FRONTAGE': 43.0, 'DEPTH': 208.0, 'useCode': '41110', 'PRE': 100.0, 'NEZ': 'WEST VILLAGE - 43', 'MTT':0, 'CIBFLAREA': 0.0, 'CIBBLDGNO': 0, 'CIBYRBUILT': 0, 'RESFLAREA': 2526, 'RESBLDGNO': 1, 'RESYRBUILT': 1914, 'RESSTYLE': 'SINGLE FAMILY', 'ISIMPROVED': 1, 'SALEPRICE': 35000.0, 'SALEDATE': '2013-06-03T00:00:00.000Z', 'ASV': 27300.0, 'ASV1': 24300.0, 'TXV': 21327.0, 'TXV1': 20828.0, 'SEV': 27300.0, 'landvalue': 13422.0, 'landMap': '464', 'RELATED': '', 'AKA': '', 'SUBDIVISION': '', 'RP': 0, 'STATUS': 'Active', 'LEGALDESC': 'S VAN DYKE PL W 25.40 FT OF 37CHAS BEWICKS SUB L21 P39 PLATS, W C R 17/550 10 EXC W 33 FT OF N 192.60 FT & EXC W 40 FT ON N LINE BG W 41.35 FT ON S LINE OF S 30.49 FT ON W LINE BG S20 FT ON E LINE 17/14 43 IRREG',
        'ownercity': 'DETROIT', 'ownerstate': 'MI', 'ownerzip': '48214', 'pnum': '17000074.001', 'propstreetcombined': '7840 VAN DYKE PL', 'resb_bldgclass': 'SINGLE FAMILY', 'resb_floorarea': 2526, 'resb_value': 27300.0, 'resb_yearbuilt': 1914, 'ownerstreetaddr': '7840 VAN DYKE PL',
    }
]

def make_bsaparceldata():

    for parceldata in bsaparceldata:

        data = parceldata.copy()
        for key in BSAPARCELDATA.HISTORICAL_VALUES.keys():
            del data[key]

        parcel = BSAPARCELDATA(**data)
        parcel.save()

    return BSAPARCELDATA.objects.first()

def make_parcel(prc_parcel_no):
    parcel = Parcel(prc_parcel_no='1000', prc_avp_no=1, prc_vp_no=1)
    parcel.save()
    return parcel


class AssessmentsTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()
        self.maxDiff = None

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
        pm = make_bsaparceldata()
        self.assertTrue(str(pm) != '')

    def test_parcelmaster_json(self):
        pm = make_bsaparceldata()
        self.assertTrue(pm.json_data() != {})

    def test_get_sales(self):

        sale = make_sale()
        c = Client()

        response = c.get('/assessments/17000074_001/')
        self.assertEqual(response.status_code, 200, "/assessments/<pnum>/ succeeds")
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 0, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
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
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 0, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
        self.assertListEqual(expected, response.data, "/assessments/<address>/ returns sales data search results")

    def test_get_sales_address_search_recent(self):

        sale = make_sale()
        c = Client()

        response = c.get('/assessments/address/7840 VAN DYKE PL/recent/')
        self.assertEqual(response.status_code, 200, "/assessments/<address>/recent/ succeeds")
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 0, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
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
        expected = [{'pnum': '17000074.001', 'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'terms': 'REVIEW NEEDED', 'instr': 'PTA', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2017, 6, 2, 0, 0, tzinfo=pytz.utc), 'saleprice': Decimal('35000'), 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY'}]
        self.assertListEqual(expected, response.data, "/assessments/<address>/recent/years/<years>/ can do custom years filter")

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
        expected = [{'grantor': 'CRABTREE, ALYSON & HIRJI, FATIMA', 'grantee': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'addresscombined': '7840 VAN DYKE PL', 'saledate': datetime(2013, 6, 3, 0, 0, tzinfo=pytz.utc), 'instr': 'PTA', 'saleprice': Decimal('35000'), 'terms': 'REVIEW NEEDED', 'pnum': '17000074.001'}]
        self.assertListEqual(expected, response.data, "/assessments/<pnum>/recent/ gets current sales")

    def test_get_sales_property_recent_filters_old(self):

        sale = make_sale()
        sale.saledate = datetime(2010, 1, 1, 0, 0, tzinfo=pytz.utc)
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

        pm = make_bsaparceldata()
        c = Client()
    
        response = c.get('/assessments/parcel/17000074_001/')
        self.assertEqual(response.status_code, 200, "/parcel/<pnum>/ succeeds")
        expected = bsaparceldata[0].copy()
        expected['field_descriptions'] = util.get_parcel_descriptions()

        self.assertDictEqual(expected, response.data, "/parcel/<pnum>/ returns data for a parcel of land")

    def test_get_parcel_property_404(self):

        c = Client()
        response = c.get('/assessments/parcel/0000/')
        self.assertEqual(response.status_code, 404, "/assessments/parcel/<pnum>/ returns 404 when property not found")

    def test_get_parcel_owner_groups(self):

        pm = make_bsaparceldata()
        c = Client()

        response = c.get('/assessments/parcel/owner_groups/')
        self.assertEqual(response.status_code, 200, "/assessments/parcel/owner_groups/ succeeds")
        expected = []
        self.assertEqual(expected, response.data, "/assessments/parcel/owner_groups/ returns layers of data for property owners")

    def test_get_rental_cases(self):

        pm = make_bsaparceldata()
        c = Client()

        parcel = Parcel(prc_parcel_no='1000', prc_avp_no=1, prc_vp_no=1)
        parcel.save()
        role_type = RoleType(role_type='Test Role Type', role_description='Role Description')
        role_type.save()
        case_type = CaseType(case_type='type-1', role_type=role_type, cst_description='Case Type')
        case_type.save()

        test_parcel1 = make_parcel(prc_parcel_no='1000')
        test_parcel2 = make_parcel(prc_parcel_no='1001')

        case_main = CaseMain.objects.create(csm_caseno=1, case_type_id='type-1', prc_parcel_no_id=test_parcel1.prc_parcel_no, csm_description='Test Case', prc_avp_no_id=test_parcel2.prc_parcel_no)
        case_main.save()

        response = c.get('/assessments/rentals/cases/1000/')
        self.assertEqual(response.status_code, 200, "/assessments/rentals/cases/<pnum>/ succeeds")
        expected = [{'csm_description': 'Test Case', 'prc_parcel_no': '1000', 'prc_avp_no': '1000', 'case_type': 'type-1', 'csm_target_date': None, 'csm_caseno': '1'}]
        self.assertListEqual(expected, response.data, "/assessments/rentals/cases/<pnum>/ returns cases for rental property")

    def test_get_rental_cases_404(self):

        c = Client()

        response = c.get('/assessments/rentals/cases/1000/')
        self.assertEqual(response.status_code, 404)

    def test_get_images(self):

        c = Client()

        sketch = Sketch(pnum='1', date=datetime(2018, 7, 30, 0, 0, tzinfo=pytz.utc), isPrimarySketch=1)
        sketch.save()

        response = c.get('/assessments/1/images/')
        self.assertEqual(response.status_code, 200)

    @skip('test_get_image fails due to desktop on network drive')
    def test_get_image(self):

        c = Client()

        sketch = Sketch(pnum='1', date=datetime(2018, 7, 30, 0, 0, tzinfo=pytz.utc), isPrimarySketch=1)

        mock_image = mock.MagicMock(spec=File, name='mock_image')
        mock_image.name='mock_image.jpg'
        sketch.imageData = mock_image
        sketch.save()

        response = c.get('/assessments/image/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_image_404(self):

        c = Client()

        response = c.get('/assessments/image/1/')
        self.assertEqual(response.status_code, 404)
