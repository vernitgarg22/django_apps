import csv, datetime, json, os, re
from datetime import datetime
import requests

from django.contrib.auth.models import User
from django.db import models
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from unittest import skip
from unittest.mock import patch
from django.test import TestCase
from django.utils.six import StringIO
from django.utils import timezone

from cod_utils.util import get_local_time

from assessments.models import ParcelMaster, Sales
from data_cache.models import DataSource, DataSet, DataValue
from photo_survey.models import Survey, Image, ImageMetadata, ParcelMetadata, PublicPropertyData
from waste_notifier.models import Subscriber
from waste_schedule.models import ScheduleDetail

from tests import test_util
from tests.test_photo_survey import cleanup_db, PhotoSurveyTests
from tests.models import TestDataA, TestDataB, TestDupe
from tests.test_data_cache import init_hydrants_data, init_gis_data, MockedGISResponse


class SendMessageTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('send_message', '5005550006', 'test message', stdout=out)
        self.assertIn("Sent message 'test message' to phone_number 5005550006", out.getvalue())


class AddUserTest(TestCase):

    def setUp(self):
        User.objects.using('photo_survey').all().delete()

    def test_command(self):

        out = StringIO()
        call_command('add_user', 'bob', 'smith', 'bob.smith@test.com', 'password', stdout=out)
        self.assertEqual(User.objects.using('photo_survey').first().email, 'bob.smith@test.com', 'add_user adds a photo_survey user')

    def test_uniqueness_enforcement(self):
        out = StringIO()
        call_command('add_user', 'bob', 'smith', 'bob.smith@test.com', 'password', stdout=out)

        with self.assertRaises(CommandError, msg="add_user should not let duplicate user be added") as error:
            call_command('add_user', 'bob', 'smith', 'bob.smith@test.com', 'password', stdout=out)


class ExportSurveyAnswersTest(TestCase):

    def setUp(self):
        cleanup_db()

    def test_output(self):

        out = StringIO()

        # Run a different test just to get a survey submitted
        PhotoSurveyTests().test_post_survey_combined()

        # add more info to parcel master
        for parcel in ParcelMaster.objects.all():
            parcel.ownername1 = 'owner name'
            parcel.ownername2 = 'other owner'
            parcel.save()

        # flesh out images
        for parcel in ParcelMetadata.objects.all():
            image = Image(file_path='/path/file.png')
            image.save()
            img_meta = ImageMetadata(image=image, parcel=parcel, created_at=get_local_time(), latitude=42.351591, longitude=-82.9988157, altitude=50)
            img_meta.save()

        # Populate public property data
        [ PublicPropertyData(parcelno=survey.parcel.parcel_id).save() for survey in Survey.objects.all() ]

        call_command('export_survey_answers', 'default_combined', stdout=out)

        PublicPropertyData.objects.all().delete()

        output = out.getvalue()
        match = re.search(r' to .*\.csv', output)
        filename = output[match.start() + 4 : match.end()]
        os.remove(filename)


class ImportPhotoSurveyImagesTest(TestCase):

    FILENAME = 'import_images.csv'

    def setUp(self):
        cleanup_db()

    @staticmethod
    def get_header():
        """
        Returns header row for image metadata csv file.
        """

        return [ "filepath","filename","longitude","latitude","altitude","gps_date","img_date","parcelno","house_numb","street_nam","street_typ","zipcode","common_nam" ]

    @staticmethod
    def get_image_data(image):
        """
        Returns data for an image.
        """

        img_meta = image.imagemetadata_set.first()
        parcel = img_meta.parcel

        return [ '/path/subdir/', 'file.png', -82.9988157, 42.351591, 50, '2017:09:05 13:15:00', 'ignored', parcel.parcel_id, 7840, "va dyke", "pl", "48214", "\"karl's house\"" ]

    def create_csv(self):
        """
        Creates csv with test data for the import.
        """

        parcel = ParcelMetadata(parcel_id='testparcelid')
        parcel.save()
        image = Image(file_path='/path/file.png')
        image.save()
        img_meta = ImageMetadata(image=image, parcel=parcel, created_at=get_local_time(), latitude=42.351591, longitude=-82.9988157, altitude=50)
        img_meta.save()

        with open(self.FILENAME, 'w', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.get_header())
            for image in Image.objects.all():
                writer.writerow(self.get_image_data(image))

    def test_import(self):

        out = StringIO()

        self.create_csv()
        cleanup_db()

        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)

        os.remove(self.FILENAME)

    def test_import_missing_parcelmetadata(self):

        out = StringIO()

        self.create_csv()

        parcel = ParcelMetadata.objects.using('photo_survey').first()

        cleanup_db()

        parcel.parcel_id = 'removed'
        parcel.save(using='photo_survey')

        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)

        os.remove(self.FILENAME)    

    def test_import_existing_metadata(self):

        out = StringIO()

        self.create_csv()
        cleanup_db()

        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)
        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)

        os.remove(self.FILENAME)

    def test_import_existing_parcel_metadata(self):

        out = StringIO()

        self.create_csv()
        parcel, created = ParcelMetadata.objects.using('photo_survey').get_or_create(parcel_id='testparcelid')
        parcel.street_name = ''
        parcel.save(using='photo_survey', force_update=True)

        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)

        os.remove(self.FILENAME)


def cleanup_db_test_commands():

    for model in ImageMetadata, Image, ParcelMetadata:
        model.objects.using('photo_survey').delete()


class ExportDataCSVTest(TestCase):

    def test_export(self):

        out = StringIO()

        cleanup_db_test_commands()

        # flesh out images
        parcel, created = ParcelMetadata.objects.using('photo_survey').get_or_create(parcel_id='testparcelid')
        image = Image(file_path='/path/file.png')
        image.save(using='photo_survey')
        img_meta = ImageMetadata(image=image, parcel=parcel, created_at=get_local_time(), latitude=42.351591, longitude=-82.9988157, altitude=50, note='Note')
        img_meta.save(using='photo_survey')

        call_command('export_data_csv', 'photo_survey', 'photo_survey', 'ImageMetadata', 'deleteme.csv', stdout=out)

        self.assertEqual(out.getvalue(), 'Wrote 1 lines to deleteme.csv\n')

        os.remove('deleteme.csv')

    def test_export_query_params(self):

        out = StringIO()

        cleanup_db_test_commands()

        # flesh out images
        parcel, created = ParcelMetadata.objects.using('photo_survey').get_or_create(parcel_id='testparcelid')
        image = Image(file_path='/path/file.png')
        image.save(using='photo_survey')
        img_meta = ImageMetadata(image=image, parcel=parcel, created_at=get_local_time(), latitude=42.351591, longitude=-82.9988157, altitude=50, note='Note')
        img_meta.save(using='photo_survey')

        call_command('export_data_csv', 'photo_survey', 'photo_survey', 'ParcelMetadata', 'deleteme.csv', '--query_params={ "parcel_id": "testparcelid" }', stdout=out)

        self.assertEqual(out.getvalue(), 'Wrote 1 lines to deleteme.csv\n')

        os.remove('deleteme.csv')

    def test_export_dedupe(self):

        out = StringIO()

        cleanup_db()

        updated_at = datetime.strptime("2017:12:01", "%Y:%m:%d")
        updated_at = timezone.make_aware(updated_at)

        test = TestDupe(dummy_id='xyz', updated_at=updated_at)
        test.save()

        updated_at = datetime.strptime("2017:12:02", "%Y:%m:%d")
        updated_at = timezone.make_aware(updated_at)

        test = TestDupe(dummy_id='xyz', updated_at=updated_at)
        test.save(force_insert=True)

        call_command('export_data_csv', 'tests', 'default', 'TestDupe', 'deleteme.csv', '--dedupe_key=dummy_id', '--order_by=updated_at', stdout=out)

        self.assertEqual(out.getvalue(), 'Wrote 1 lines to deleteme.csv\n')

        os.remove('deleteme.csv')

    def test_output_foreign_key(self):

        out = StringIO()

        test_data_a = TestDataA(data='data')
        test_data_a.save()
        test_data_b = TestDataB(test_data_a=test_data_a, data='data')
        test_data_b.save()

        test_data_a.delete()

        call_command('export_data_csv', 'tests', 'default', 'TestDataB', 'test_data_b.csv', stdout=out)

        self.assertEqual(out.getvalue(), 'Wrote 1 lines to test_data_b.csv\n')

        os.remove('test_data_b.csv')


class RefreshDataCacheTest(TestCase):

    def setUp(self):

        test_util.cleanup_model(DataValue)
        test_util.cleanup_model(DataSource)
        test_util.cleanup_model(DataSet)

    def tearDown(self):

        test_util.cleanup_model(DataValue)
        test_util.cleanup_model(DataSource)
        test_util.cleanup_model(DataSet)

    @skip('old hydrant data no longer available')
    def test_simple_data(self):
        """
        Test data cache where there is only 1 data value per data source (i.e., no param).
        """

        init_hydrants_data()
        self.assertEqual(DataSource.objects.first().datavalue_set.count(), 0)

        call_command('refresh_data_cache')

        # TODO we may be getting a race condition here - call shutdown first?

        self.assertEqual(DataSource.objects.first().datavalue_set.count(), 1)

    def test_multiple_data(self):
        """
        Test data cache where there can be multiple data value objects per data source (i.e., with a param).
        """

        init_gis_data()
        self.assertEqual(DataSource.objects.first().datavalue_set.count(), 0)

        with patch.object(requests, 'post', return_value=MockedGISResponse()), patch.object(requests, 'get', return_value=MockedGISResponse()):
            call_command('refresh_data_cache')

        self.assertEqual(DataSource.objects.first().datavalue_set.count(), 1)


class SendWasteRemindersTest(TestCase):

    def test0(self):

        out = StringIO()
        call_command('send_waste_reminders', stdout=out)
        self.assertTrue(out.getvalue().find('"status": 200') >= 0)

    def test1(self):

        out = StringIO()

        subscriber = Subscriber(phone_number="5005550006", waste_area_ids="0", address="1105 Military St", service_type="all")
        subscriber.activate()

        call_command('send_waste_reminders', '--today=20170521', stdout=out)

        expected = {"status":200,"data":{"meta":{"date_applicable":"2017-05-22","week_type":"b","current_time":datetime.today().strftime("%Y-%m-%d %H:%M"),"dry_run":True},"all":{"0":{"message":"City of Detroit Public Works:  Your next pickup for bulk, recycling and trash is Monday, May 22, 2017 (reply with REMOVE ME to cancel pickup reminders; begin your reply with FEEDBACK to give us feedback on this service).","subscribers":["5005550006"]}}}}
        data = json.loads(out.getvalue())

        self.assertEqual(data, expected)

    def test2(self):

        with self.assertRaises(CommandError, msg="--dry_run must be 'yes' or 'no'") as error:
            call_command('send_waste_reminders', '--dry_run=True')

    def test3(self):

        with self.assertRaises(CommandError, msg="Date format for 'today' must be YYYYMMDD") as error:
            call_command('send_waste_reminders', '--today=171007')
