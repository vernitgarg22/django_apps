from datetime import datetime
import json

from django.test import Client
from django.test import TestCase

import tests.disabled

from photo_survey.models import Image, ImageMetadata
from photo_survey.models import SurveyTemplate, SurveyData
import photo_survey.views


def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(Image)
    cleanup_model(ImageMetadata)
    cleanup_model(SurveyTemplate)
    cleanup_model(SurveyData)

def build_image_data():
    image = Image(file_path='demoimage1.jpg')
    image.save()
    image_metadata = ImageMetadata(image=image, parcel_id='testparcelid', created_at=datetime.now(), note='test image')
    image_metadata.save()

def build_survey_template():
    data = [
        { "survey_template_id": "default", "question_id": "parcel_id", "question_number": 1, "question_text": "Location information", "valid_answers": ".*" },
        { "survey_template_id": "default", "question_id": "needs_intervention", "question_number": 2, "question_text": "Does this parcel need intervention?", "valid_answers": "y|n" },
        { "survey_template_id": "default", "question_id": "lot_or_structure", "question_number": 3, "question_text": "Is the blighted parcel a lot or structure?", "valid_answers": "lot|structure" },
        { "survey_template_id": "default", "question_id": "structure_with_blight", "question_number": 4, "question_text": "Structure with Blight", "valid_answers": "[a-c,]" },
        { "survey_template_id": "default", "question_id": "elements_of_structure", "question_number": 5, "question_text": "Elements of the Blighted Structure", "valid_answers": "[a-o,]+" },
        { "survey_template_id": "default", "question_id": "elements_of_lot", "question_number": 6, "question_text": "Elements of the Blighted Lot", "valid_answers": "[a-m,]+" },
    ]

    for row in data:
        template = SurveyTemplate(**row)
        template.save()

def get_default_survey_answers():
    return {
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

class PhotoSurveyTests(TestCase):

    def setUp(self):
        cleanup_db()
        build_image_data()
        self.maxDiff = None

    def test_get_survey_count(self):
        c = Client()

        response = c.get('/photo_survey/count/testparcelid/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({ "count": 1 }, response.data, "/photo_survey/count/<parce id>/ returns number of surveys available for the given parcel")

    def test_get_survey_metadata(self):
        c = Client()

        response = c.get('/photo_survey/testparcelid/')
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

        build_survey_template()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_default_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers")

    def test_post_survey_invalid_data(self):

        build_survey_template()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][0]['answer'] = ''

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid data")
        self.assertEqual({'parcel_id': 'question answer is invalid'}, response.data, "Parcel id is identified as invalid")

    def test_post_survey_missing_data(self):

        build_survey_template()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][0] = { "question_id": "parcel_id_xyz", "answer": "<test_parcel_id>" }

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid data")
        self.assertEqual({'parcel_id': 'question answer is required'}, response.data, "Parcel id is identified as required")
