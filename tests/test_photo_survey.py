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
        { "survey_template_id": "default", "question_id": "parcel_id", "question_number": 1, "question_text": "Location information", "valid_answers": ".*", "required_by": "y" },
        { "survey_template_id": "default", "question_id": "needs_intervention", "question_number": 2, "question_text": "Does this parcel need intervention?", "valid_answers": "y|n", "required_by": "y", "answer_trigger": "n", "answer_trigger_action": "exit" },
        { "survey_template_id": "default", "question_id": "lot_or_structure", "question_number": 3, "question_text": "Is the blighted parcel a lot or structure?", "valid_answers": "lot|structure", "required_by": "needs_intervention", "required_by_answer": "y" },
        { "survey_template_id": "default", "question_id": "structure_with_blight", "question_number": 4, "question_text": "Structure with Blight", "valid_answers": "[a-c,]", "required_by": "lot_or_structure", "required_by_answer": "structure" },
        { "survey_template_id": "default", "question_id": "elements_of_structure", "question_number": 5, "question_text": "Elements of the Blighted Structure", "valid_answers": "[a-o,]+", "required_by": "lot_or_structure", "required_by_answer": "structure" },
        { "survey_template_id": "default", "question_id": "elements_of_lot", "question_number": 6, "question_text": "Elements of the Blighted Lot", "valid_answers": "[a-m,]+", "required_by": "lot_or_structure", "required_by_answer": "lot" },
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

def get_lot_ok_survey_answers():
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
          "answer": "n"
        }
      ]
    }

def get_lot_bad_survey_answers():
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
          "answer": "lot"
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

def get_structure_bad_survey_answers():
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
        }
      ]
    }

def get_edgars_survey_answers():
    return {
      "survey_id": "default",
      "user_id": "xyz",
      "answers": [
        {
          "question_id": "parcel_id",
          "answer": "testparcelid"
        },
        {
          "question_id": "needs_intervention",
          "answer": "y"
        },
        {
          "question_id": "lot_or_structure",
          "answer": "lot"
        },
        {
          "question_id": "elements_of_lot",
          "answer": "b,d,h,j"
        }
      ]
    }


class PhotoSurveyUtilTests(TestCase):

    def test_answer_not_required(self):
        question = SurveyTemplate(survey_template_id='test', question_id='optional_info', question_number=1, question_text='Any extra info?', valid_answers='.*', required_by='n')
        self.assertFalse(photo_survey.views.is_answer_required(question, { "question_id": "optional_info", "answer": "" }), "is_answer_required() identifies optional answers")


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

    def test_post_survey_parcel_ok(self):

        build_survey_template()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_lot_ok_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when lot does not need intervention")

    def test_post_survey_lot_bad(self):

        build_survey_template()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_lot_bad_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when lot needs intervention")

    def test_post_survey_structure_bad(self):

        build_survey_template()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_structure_bad_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when structure needs intervention")

    def test_post_survey_invalid_data(self):

        build_survey_template()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][0]['answer'] = ''

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid data")
        self.assertEqual({'parcel_id': 'question answer is invalid'}, response.data, "Parcel id is identified as invalid")

    def test_post_survey_structure_edgar(self):

        build_survey_template()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_edgars_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers from edgar")

    def test_post_survey_missing_data(self):

        build_survey_template()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][0] = { "question_id": "parcel_id_xyz", "answer": "<test_parcel_id>" }

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags missing data")
        self.assertEqual({'parcel_id': 'question answer is required'}, response.data, "Parcel id is identified as required")
