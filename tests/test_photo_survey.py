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

    def test_post_survey(self):
        c = Client()

        survey_answer_data = {
            "survey_id": "default",
            "user_id": "xyz",
            "answers": [
            {
              "question_id": "parcel_id",
              "answer": "<test_parcel_id>"
            },
            {
              "question_id": "needs_intervention",
              "answer": "y"
            },
            {
              "question_id": "lot_or_structure",
              "answer": "structure"
            },
            {
              "question_id": "structure_with_blight",
              "answer": "a"
            },
            {
              "question_id": "elements_of_structure",
              "answer": "b,c,d"
            },
            {
              "question_id": "elements_of_lot",
              "answer": "a,f"
            }
          ]
        }

        response = c.post('/photo_survey/survey/test_parcel_id/', survey_answer_data)
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers")
        # self.assertEqual(True, True, "/photo_survey/survey/ stores field survey answers")
