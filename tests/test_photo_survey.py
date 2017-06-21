from datetime import datetime

from django.test import Client
from django.test import TestCase

import tests.disabled

from photo_survey.models import Image, ImageMetadata
import photo_survey.views


def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(Image)
    cleanup_model(ImageMetadata)

def build_image_data():
    image = Image(file_path='demoimage1.jpg')
    image.save()
    image_metadata = ImageMetadata(image=image, parcel_id='test_parcel_id', created_at=datetime.now(), note='test image')
    image_metadata.save()


class PhotoSurveyTests(TestCase):

    def setUp(self):
        cleanup_db()
        build_image_data()
        self.maxDiff = None

    def test_get_survey_count(self):
        c = Client()

        response = c.get('/photo_survey/count/test_parcel_id/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({ "count": 1 }, response.data, "/photo_survey/count/<parce id>/ returns number of surveys available for the given parcel")

    def test_get_survey_metadata(self):
        c = Client()

        response = c.get('/photo_survey/test_parcel_id/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'images': ['demoimage1']}, response.data, "/photo_survey/<parce id>/ returns metadata about information available for the given parcel")

    def test_get_image(self):
        c = Client()

        response = c.get('/photo_survey/image/demoimage1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3002556, len(response.data), "/photo_survey/image/<image id>/ returns an image")

    def test_get_image_404(self):
        c = Client()

        response = c.get('/photo_survey/image/wrong/')
        self.assertEqual(response.status_code, 404)
