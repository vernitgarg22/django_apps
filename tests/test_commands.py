import csv, os, re

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase
from django.utils.six import StringIO

from cod_utils.util import get_local_time

from assessments.models import ParcelMaster
from photo_survey.models import Survey, Image, ImageMetadata, ParcelMetadata, PublicPropertyData

from tests.test_photo_survey import cleanup_db, PhotoSurveyTests


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

    def test_import_existing_metadata(self):

        out = StringIO()

        self.create_csv()
        cleanup_db()

        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)
        call_command('import_image_metadata', self.FILENAME, 'photo_survey', stdout=out)

        os.remove(self.FILENAME)
