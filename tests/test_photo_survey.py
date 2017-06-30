from datetime import datetime
import json

from django.test import Client
from django.test import TestCase

import tests.disabled

from photo_survey.models import Image, ImageMetadata
from photo_survey.models import SurveyQuestion, SurveyAnswer
from assessments.models import ParcelMaster

import photo_survey.views


def cleanup_model(model):
    model.objects.all().delete()

def init_parcel_master(parcel_id = 'testparcelid'):
    data = {'resb_priceground': 29.04669, 'resb_occ': 0, 'cib_effage': 0, 'resb_depr': 38, 'propstreetcombined': '7840 VAN DYKE PL', 'cib_floorarea': 0.0, 'resb_value': 37325.0, 'cib_numcib': 0, 'resb_style': 'SINGLE FAMILY', 'cib_calcvalue': 0.0, 'cib_pricefloor': 0.0, 'resb_heat': 2, 'resb_calcvalue': 106948.421875, 'resb_nbed': 0, 'resb_exterior': 3, 'ownerstate': 'MI', 'ownercity': 'DETROIT', 'resb_pricefloor': 13.31134, 'resb_gartype': 1, 'resb_yearbuilt': 1914, 'resb_garagearea': 504, 'resb_groundarea': 1285, 'resb_fireplaces': 1, 'resb_styhgt': 5, 'resb_basementarea': 1110, 'resb_bldgclass': 2, 'cib_yearbuilt': 0, 'ownername2': '', 'relatedpnum': '', 'resb_avestyht': 2.1821, 'resb_plusminus': 0, 'cib_bldgclass': 0, 'pnum': parcel_id, 'resb_effage': 52, 'resb_fullbaths': 2, 'resb_floorarea': 2804, 'cib_occ': 0, 'cibunits': 0, 'resb_halfbaths': 1, 'ownerstreetaddr': '7840 VAN DYKE PL', 'cibbedrooms': 0, 'ownerzip': '48214', 'ownername1': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'xstreetname_1': 'SEYBURN', 'xstreetname_0': 'VAN DYKE', 'resb_numresb': 1, 'cib_stories': 0, 'cib_value': 0.0}
    pm = ParcelMaster(**data)
    pm.save()
    return pm


def cleanup_db():
    cleanup_model(Image)
    cleanup_model(ImageMetadata)
    cleanup_model(SurveyQuestion)
    cleanup_model(SurveyAnswer)
    cleanup_model(ParcelMaster)

def build_image_data():
    image = Image(file_path='demoimage1.jpg')
    image.save()

    image_metadata = ImageMetadata(image=image, parcel_id='testparcelid', created_at=datetime.now(), latitude=0, longitude=0, altitude=0, note='test image')
    image_metadata.save()

# TODO rename these
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
        template = SurveyQuestion(**row)
        template.save()

def build_survey_template_combined():
    data = [
        { "survey_template_id": "default_combined", "question_id": "is_structure_on_site",         "question_number": 1,  "question_text": "Is there a structure on site?",                              "valid_answers": "y|n",     "required_by": "",                          "required_by_answer": "" },
        { "survey_template_id": "default_combined", "question_id": "is_structure_occupied",        "question_number": 2,  "question_text": "Is the structure occupied?",                                 "valid_answers": "[a-d]",   "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_template_id": "default_combined", "question_id": "site_use_type",                "question_number": 3,  "question_text": "What is the site used for?",                                 "valid_answers": "[a-f]",   "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_template_id": "default_combined", "question_id": "num_residential_units",        "question_number": 4,  "question_text": "How many residential units?",                                "valid_answers": "[a-d]",   "required_by": "site_use_type",             "required_by_answer": "a" },
        { "survey_template_id": "default_combined", "question_id": "residence_type",               "question_number": 5,  "question_text": "What type of residences?",                                   "valid_answers": "[a-c]",   "required_by": "site_use_type",             "required_by_answer": "a" },
        { "survey_template_id": "default_combined", "question_id": "commercial_occupants_type",    "question_number": 6,  "question_text": "What type of commercial occupant(s)?",                       "valid_answers": "[a-h]",   "required_by": "site_use_type",             "required_by_answer": "b|c" },
        { "survey_template_id": "default_combined", "question_id": "industrial_occupants_type",    "question_number": 7,  "question_text": "What type of industrial occupant(s)?",                       "valid_answers": "[a-d]",   "required_by": "site_use_type",             "required_by_answer": "d" },
        { "survey_template_id": "default_combined", "question_id": "institutional_occupants_type", "question_number": 8,  "question_text": "What type of institutional occupant(s)?",                    "valid_answers": "[a-h]",   "required_by": "site_use_type",             "required_by_answer": "e" },
        { "survey_template_id": "default_combined", "question_id": "structure_condition",          "question_number": 9,  "question_text": "What is the condition of the structure?",                    "valid_answers": "[a-d]",   "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_template_id": "default_combined", "question_id": "is_structure_fire_damaged",    "question_number": 10, "question_text": "Is the structure fire damaged?",                             "valid_answers": "y|n",     "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_template_id": "default_combined", "question_id": "fire_damage_level",            "question_number": 11, "question_text": "What is the level of fire damage?",                          "valid_answers": "[a-c]",   "required_by": "is_structure_fire_damaged", "required_by_answer": "y" },
        { "survey_template_id": "default_combined", "question_id": "is_structure_secure",          "question_number": 12, "question_text": "Is the building secure or open to trespass?",                "valid_answers": "y|n",     "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_template_id": "default_combined", "question_id": "site_use",                     "question_number": 13, "question_text": "What is the site used for?",                                 "valid_answers": "[a-f]",   "required_by": "",                          "required_by_answer": "" },
        { "survey_template_id": "default_combined", "question_id": "is_lot_maintained",            "question_number": 14, "question_text": "Is the lot maintained?",                                     "valid_answers": "y|n",     "required_by": "",                          "required_by_answer": "" },
        { "survey_template_id": "default_combined", "question_id": "is_dumping_on_site",           "question_number": 15, "question_text": "Is there dumping on the site?",                              "valid_answers": "y|n",     "required_by": "",                          "required_by_answer": "" },
        { "survey_template_id": "default_combined", "question_id": "blighted_lot_elements",        "question_number": 16, "question_text": "Elements of the blighted lot (select all that apply)",       "valid_answers": "[a-m,]+", "required_by": "n" },
        { "survey_template_id": "default_combined", "question_id": "blighted_structure_elements",  "question_number": 17, "question_text": "Elements of the blighted structure (select all that apply)", "valid_answers": "[a-o,]+", "required_by": "n" },
    ]

    for row in data:
        template = SurveyQuestion(**row)
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

def get_combined_survey_answers():
    return {
        "survey_id": "default_combined",
        "user_id": "xyz",
        "answers": [
            { "question_id": "is_structure_on_site", "answer": "y" },
            { "question_id": "is_structure_occupied", "answer": "a" },
            { "question_id": "site_use_type", "answer": "b" },
            { "question_id": "num_residential_units", "answer": "" },
            { "question_id": "residence_type", "answer": "" },
            { "question_id": "commercial_occupants_type", "answer": "a" },
            { "question_id": "industrial_occupants_type", "answer": "" },
            { "question_id": "institutional_occupants_type", "answer": "" },
            { "question_id": "structure_condition", "answer": "b" },
            { "question_id": "is_structure_fire_damaged", "answer": "n" },
            { "question_id": "fire_damage_level", "answer": "" },
            { "question_id": "is_structure_secure", "answer": "y" },
            { "question_id": "site_use", "answer": "e" },
            { "question_id": "is_lot_maintained", "answer": "y" },
            { "question_id": "is_dumping_on_site", "answer": "n" },
            { "question_id": "blighted_lot_elements", "answer": "" },
            { "question_id": "blighted_structure_elements", "answer": "" }
        ],
        "parcel_ids": [
          "testparcelid",
          "nearby_parcel_id"
        ]
    }


class PhotoSurveyUtilTests(TestCase):

    def test_answer_not_required(self):
        question = SurveyQuestion(survey_template_id='test', question_id='optional_info', question_number=1, question_text='Any extra info?', valid_answers='.*', required_by='n')
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
        self.assertEqual({'images': ['http://testserver/data/photo_survey/images/demoimage1.jpg']}, response.data, "/photo_survey/<parce id>/ returns metadata about information available for the given parcel")

    def test_post_survey(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_default_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers")

    def test_post_survey_combined(self):

        build_survey_template_combined()
        init_parcel_master()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores combined field survey answers")
        self.assertEqual(response.data['parcel_survey_info'], { 'nearby_parcel_id': 0, 'testparcelid': 1 }, "/photo_survey/survey/ returns info about existing surveys")

    def test_post_survey_parcel_ok(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_lot_ok_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when lot does not need intervention")

    def test_post_survey_lot_bad(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_lot_bad_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when lot needs intervention")

    def test_post_survey_structure_bad(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_structure_bad_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when structure needs intervention")

    def test_post_survey_invalid_parcel_id(self):

        build_survey_template_combined()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ stores combined field survey answers")
        self.assertEqual({'invalid parcel id': 'testparcelid'}, response.data, "Parcel id is identified as invalid")

    def test_post_survey_invalid_data(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][1]['answer'] = 'x'

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid data")
        self.assertEqual({'needs_intervention': 'question answer is invalid'}, response.data, "Parcel id is identified as invalid")

    def test_post_survey_missing_data(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][0] = { "question_id": "parcel_id", "answer": "" }

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags missing data")
        self.assertEqual({'parcel_id': 'question answer is required'}, response.data, "Parcel id is identified as required")

    def test_invalid_survey_template(self):
        c = Client()

        init_parcel_master()

        survey_answers = get_default_survey_answers()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid survey template")
        self.assertEqual({'invalid survey': 'default'}, response.data, "Parcel id is identified as required")

    def test_invalid_question_ids(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'].append({ "question_id": "invalid", "answer": "" })

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid survey template")
        self.assertEqual({'invalid question ids': ['invalid']}, response.data, "Parcel id is identified as required")

    def test_post_survey_structure_edgar(self):

        build_survey_template()
        init_parcel_master()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_edgars_survey_answers()), content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers from edgar")