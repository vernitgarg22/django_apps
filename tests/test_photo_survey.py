import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.test import Client
from django.test import TestCase

import tests.disabled
from tests import test_util

from photo_survey.models import Image, ImageMetadata
from photo_survey.models import ParcelMetadata, Survey, SurveyType, SurveyQuestion, SurveyAnswer, SurveyQuestionAvailAnswer
from assessments.models import ParcelMaster

from cod_utils.util import date_json

import photo_survey.views
from photo_survey.views import authenticate_user


def init_parcel_data(parcel_id = 'testparcelid'):
    data = {'resb_priceground': 29.04669, 'resb_occ': 0, 'cib_effage': 0, 'resb_depr': 38, 'propstreetcombined': '7840 VAN DYKE PL', 'cib_floorarea': 0.0, 'resb_value': 37325.0, 'cib_numcib': 0, 'resb_style': 'SINGLE FAMILY', 'cib_calcvalue': 0.0, 'cib_pricefloor': 0.0, 'resb_heat': 2, 'resb_calcvalue': 106948.421875, 'resb_nbed': 0, 'resb_exterior': 3, 'ownerstate': 'MI', 'ownercity': 'DETROIT', 'resb_pricefloor': 13.31134, 'resb_gartype': 1, 'resb_yearbuilt': 1914, 'resb_garagearea': 504, 'resb_groundarea': 1285, 'resb_fireplaces': 1, 'resb_styhgt': 5, 'resb_basementarea': 1110, 'resb_bldgclass': 2, 'cib_yearbuilt': 0, 'ownername2': '', 'relatedpnum': '', 'resb_avestyht': 2.1821, 'resb_plusminus': 0, 'cib_bldgclass': 0, 'pnum': parcel_id, 'resb_effage': 52, 'resb_fullbaths': 2, 'resb_floorarea': 2804, 'cib_occ': 0, 'cibunits': 0, 'resb_halfbaths': 1, 'ownerstreetaddr': '7840 VAN DYKE PL', 'cibbedrooms': 0, 'ownerzip': '48214', 'ownername1': 'KAEBNICK,KARL ROYDEN & HAIMERI, AMY', 'xstreetname_1': 'SEYBURN', 'xstreetname_0': 'VAN DYKE', 'resb_numresb': 1, 'cib_stories': 0, 'cib_value': 0.0}
    pm = ParcelMaster(**data)
    pm.save()

    ParcelMetadata.objects.get_or_create(parcel_id=parcel_id)[0].save()

    return pm

def cleanup_db():
    test_util.cleanup_model(ImageMetadata)
    test_util.cleanup_model(Image)
    test_util.cleanup_model(SurveyAnswer)
    test_util.cleanup_model(SurveyQuestionAvailAnswer)
    test_util.cleanup_model(SurveyQuestion)
    test_util.cleanup_model(Survey)
    test_util.cleanup_model(SurveyType)
    test_util.cleanup_model(ParcelMetadata)
    test_util.cleanup_model(ParcelMaster, 'default')
    test_util.cleanup_model(Token)
    test_util.cleanup_model(User, using='photo_survey')
    test_util.cleanup_model(ParcelMaster)

def build_image_data(parcel_id='test_parcel_id'):

    parcel, created = ParcelMetadata.objects.get_or_create(parcel_id=parcel_id)
    parcel.save()

    image = Image(file_path='demoimage1.jpg')
    image.save()

    image_metadata = ImageMetadata(image=image, parcel=parcel, created_at=timezone.now(), latitude=0, longitude=0, altitude=0, note='test image')
    image_metadata.save()

def create_user(email='lennon@thebeatles.com', password='johnpassword'):
    # Note: we are using email for username
    user = User.objects.using('photo_survey').filter(email=email).first()
    if not user:
        user = User.objects.db_manager('photo_survey').create_user(email, email, password)
    return user

# TODO rename these
def build_survey_template():

    survey_type = SurveyType(survey_template_id='default')
    survey_type.save()

    data = [
        { "survey_type": survey_type, "question_id": "parcel_id", "question_number": 1, "question_text": "Location information", "valid_answers": ".*", "required_by": "y" },
        { "survey_type": survey_type, "question_id": "needs_intervention", "question_number": 2, "question_text": "Does this parcel need intervention?", "valid_answers": "y|n", "required_by": "y", "answer_trigger": "n", "answer_trigger_action": "exit" },
        { "survey_type": survey_type, "question_id": "lot_or_structure", "question_number": 3, "question_text": "Is the blighted parcel a lot or structure?", "valid_answers": "lot|structure", "required_by": "needs_intervention", "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "structure_with_blight", "question_number": 4, "question_text": "Structure with Blight", "valid_answers": "[a-c,]", "required_by": "lot_or_structure", "required_by_answer": "structure" },
        { "survey_type": survey_type, "question_id": "elements_of_structure", "question_number": 5, "question_text": "Elements of the Blighted Structure", "valid_answers": "[a-o,]+", "required_by": "lot_or_structure", "required_by_answer": "structure" },
        { "survey_type": survey_type, "question_id": "elements_of_lot", "question_number": 6, "question_text": "Elements of the Blighted Lot", "valid_answers": "[a-m,]+", "required_by": "lot_or_structure", "required_by_answer": "lot" },
    ]

    for row in data:
        template = SurveyQuestion(**row)
        template.save()

def build_survey_template_combined():

    parcel, created = ParcelMetadata.objects.get_or_create(parcel_id='testparcelid')
    parcel.save()

    survey_type = SurveyType(survey_template_id='default_combined')
    survey_type.save()

    data = [
        { "survey_type": survey_type, "question_id": "is_structure_on_site",         "question_number": 1,  "question_text": "Is there a structure on site?",                              "valid_answers": "y|n",     "required_by": "",                          "required_by_answer": "" },
        { "survey_type": survey_type, "question_id": "is_structure_occupied",        "question_number": 2,  "question_text": "Is the structure occupied?",                                 "valid_answers": "[a-d]",   "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "site_use_type",                "question_number": 3,  "question_text": "What is the site used for?",                                 "valid_answers": "[a-f]",   "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "num_residential_units",        "question_number": 4,  "question_text": "How many residential units?",                                "valid_answers": "[a-d]",   "required_by": "site_use_type",             "required_by_answer": "a" },
        { "survey_type": survey_type, "question_id": "residence_type",               "question_number": 5,  "question_text": "What type of residences?",                                   "valid_answers": "[a-c]",   "required_by": "site_use_type",             "required_by_answer": "a" },
        { "survey_type": survey_type, "question_id": "commercial_occupants_type",    "question_number": 6,  "question_text": "What type of commercial occupant(s)?",                       "valid_answers": "[a-h]",   "required_by": "site_use_type",             "required_by_answer": "b|c" },
        { "survey_type": survey_type, "question_id": "industrial_occupants_type",    "question_number": 7,  "question_text": "What type of industrial occupant(s)?",                       "valid_answers": "[a-d]",   "required_by": "site_use_type",             "required_by_answer": "d" },
        { "survey_type": survey_type, "question_id": "institutional_occupants_type", "question_number": 8,  "question_text": "What type of institutional occupant(s)?",                    "valid_answers": "[a-h]",   "required_by": "site_use_type",             "required_by_answer": "e" },
        { "survey_type": survey_type, "question_id": "structure_condition",          "question_number": 9,  "question_text": "What is the condition of the structure?",                    "valid_answers": "[a-d]",   "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "is_structure_fire_damaged",    "question_number": 10, "question_text": "Is the structure fire damaged?",                             "valid_answers": "y|n",     "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "fire_damage_level",            "question_number": 11, "question_text": "What is the level of fire damage?",                          "valid_answers": "[a-c]",   "required_by": "is_structure_fire_damaged", "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "is_structure_secure",          "question_number": 12, "question_text": "Is the building secure or open to trespass?",                "valid_answers": "y|n",     "required_by": "is_structure_on_site",      "required_by_answer": "y" },
        { "survey_type": survey_type, "question_id": "site_use",                     "question_number": 13, "question_text": "What is the site used for?",                                 "valid_answers": "[a-f]",   "required_by": "",                          "required_by_answer": "" },
        { "survey_type": survey_type, "question_id": "is_lot_maintained",            "question_number": 14, "question_text": "Is the lot maintained?",                                     "valid_answers": "y|n",     "required_by": "",                          "required_by_answer": "" },
        { "survey_type": survey_type, "question_id": "is_dumping_on_site",           "question_number": 15, "question_text": "Is there dumping on the site?",                              "valid_answers": "y|n",     "required_by": "",                          "required_by_answer": "" },
        { "survey_type": survey_type, "question_id": "blighted_lot_elements",        "question_number": 16, "question_text": "Elements of the blighted lot (select all that apply)",       "valid_answers": "[a-m,]+", "required_by": "n",                         "scoring_type": "sum" },
        { "survey_type": survey_type, "question_id": "blighted_structure_elements",  "question_number": 17, "question_text": "Elements of the blighted structure (select all that apply)", "valid_answers": "[a-o,]+", "required_by": "n",                         "scoring_type": "sum" },
        # { "survey_type": survey_type, "question_id": "sidewalk_condition",           "question_number": 18, "question_text": "Is the sidewalk/curb: (select all that apply)",              "valid_answers": "[a-d,]+", "required_by": "" },
    ]

    survey_questions = []

    for row in data:
        survey_question = SurveyQuestion(**row)
        survey_question.save()
        survey_questions.append(survey_question)

    survey_question = survey_questions[0]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[1]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[2]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[3]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[4]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[5]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[6]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[7]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[8]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[9]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[10]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[11]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[12]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[13]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[14]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[15]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Active billboard', weight=1)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Inactive billboard', weight=1)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Lot is accessible', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='i', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='j', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='k', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='l', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='m', text='', weight=0)
    avail_answer.save()

    survey_question = survey_questions[16]
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Needs Demo', weight=1)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Needs Board Up', weight=1)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Structure is accessible', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='i', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='j', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='k', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='l', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='m', text='', weight=0)
    avail_answer.save()
    avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='o', text='', weight=0)
    avail_answer.save()

    # survey_question = survey_questions[17]
    # avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='', weight=0)
    # avail_answer.save()
    # avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='', weight=0)
    # avail_answer.save()
    # avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='', weight=0)
    # avail_answer.save()
    # avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='', weight=0)
    # avail_answer.save()

# value   text    survey_question_id  Weight
# 0
# y   Yes 7   0
# n   No  7   0

# 1
# a   Occupied    8   0
# b   Unoccupied  8   0
# c   Partially Occupied  8   0
# d   Possibly Unoccupied 8   0

# 2
# a   Residential 9   0
# b   Commercial  9   0
# c   Mixed-use   9   0
# d   Industrial  9   0
# e   Institutional   9   0
# f   Unknown 9   0

# 3
# a   Garage or shed  10  0
# b   Single Family   10  0
# c   Multi-Family    10  0
# d   Apartments  10  0

# 4
# a   Single Family   11  0
# b   Multi-Family    11  0
# c   Apartments  11  0

# 5
# a   Restaurant / Bar    12  0
# b   Grocery 12  0
# c   Retail  12  0
# d   Service 12  0
# e   Offices 12  0
# f   Entertainment   12  0
# g   Multi-Occupant  12  0
# h   Other   12  0

# 6
# a   Industrial  13  0
# b   Warehouses  13  0
# c   Multi-Occupant  13  0
# d   Other   13  0

# 7
# a   Schools 14  0
# b   Religious   14  0
# c   Public Safety   14  0
# d   Health  14  0
# e   Recreation  14  0
# f   Government  14  0
# g   Non-Profit/Charity  14  0
# h   Other   14  0

# 8
# a   Good    15  0
# b   Fair    15  1
# c   Poor    15  3
# d   Suggest Demolition  15  5

# 9
# y   Yes 16  0
# n   No  16  0

# 10
# a   Minor   17  1
# b   Major   17  3
# c   Collapsed   17  5

# 11
# y   Secured 18  0
# n   Open to Trespass    18  2

# 12
# a   Vacant Lot  19  0
# b   Parking Lot 19  0
# c   Park    19  0
# d   Garden  19  0
# e   Other   19  0
# f   Attached Lot    19  0

# 13
# y   Yes 20  0
# n   No  20  2

# 14
# y   Yes 21  0
# n   No  21  0

# 15
# a   Active billboard    22  1
# b   Inactive billboard  22  1
# c   Lot is accessible   22  0
# d   Blighted signs  22  1
# e   Graffiti    22  1
# f   Overgrown   22  1
# g   Cement piles    22  1
# h   Large dirt piles    22  1
# i   Tires illegally dumped  22  1
# j   Broken/abandoned fences 22  1
# k   Abandoned cars (2 or less)  22  1
# l   Abandoned cars (3 or more)  22  2
# m   Other   22  1

# 16
# a   Needs Demo  23  5
# b   Needs Board Up  23  3
# c   Structure is accessible 23  0
# d   Active billboard    23  1
# e   Inactive billboard  23  1
# f   Blighted signs/awnings  23  1
# g   Graffiti, etc   23  1
# h   Overgrown   23  1
# i   Cement piles    23  1
# j   Large Dirt piles    23  1
# k   Tires illegaly dumped   23  1
# l   Broken/abandoned fences 23  1
# m   Abandoned cars (2 or less)  23  1
# n   Abandoned cars (3 or more)  23  2
# o   Other   23  1

# 17
# a   Cracked 24  0
# b   Uneven over 1.5"    24  0
# c   Missing 24  0
# d   Appears in good condition   24  0





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
            { "question_id": "blighted_lot_elements", "answer": "a,b,c" },
            { "question_id": "blighted_structure_elements", "answer": "" }
        ],
        "parcel_ids": [
          "testparcelid",
          "nearby_parcel_id"
        ]
    }

def create_survey(parcel_id = 'testparcelid'):

    parcel = ParcelMetadata(parcel_id=parcel_id)
    parcel.save()
    survey_type = SurveyType(survey_template_id='default_combined')
    survey_type.save()
    survey = Survey(parcel=parcel, survey_type=survey_type)
    survey.save()
    return survey


class PhotoSurveyAuthTests(TestCase):

    def setUp(self):
        cleanup_db()

    def test_get_auth_token(self):

        create_user()

        c = Client()
        data = { "email": "lennon@thebeatles.com", "password": "johnpassword" }
        response = c.post('/photo_survey/auth_token/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/auth_token/ creates an authentication token")
        self.assertTrue(len(response.data['token']) > 0, "/photo_survey/get_auth_token/ returns json with an authentication token")

    def test_get_auth_token_not_secure(self):

        create_user()

        c = Client()
        data = { "email": "lennon@thebeatles.com", "password": "johnpassword" }
        response = c.post('/photo_survey/auth_token/', json.dumps(data), secure=False, content_type="application/json")
        self.assertEqual(response.status_code, 403, "/photo_survey/auth_token/ requires https")

    def test_get_auth_token_bad_user(self):

        create_user()

        c = Client()
        data = { "email": "wrong@thebeatles.com", "password": "johnpassword" }
        response = c.post('/photo_survey/auth_token/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 401, "/photo_survey/auth_token/ requires correct email/password combo")

    def test_get_auth_token_bad_password(self):

        create_user()

        c = Client()
        data = { "email": "lennon@thebeatles.com", "password": "wrong" }
        response = c.post('/photo_survey/auth_token/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 401, "/photo_survey/auth_token/ requires correct email/password combo")

    def test_get_auth_token_error_handling(self):
        c = Client()
        data = { "email": "lennon@thebeatles.com" }
        response = c.post('/photo_survey/auth_token/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/auth_token/ requires email and password")

    def test_get_auth_token_no_data(self):
        c = Client()
        response = c.post('/photo_survey/auth_token/', secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/auth_token/ requires data")


class PhotoSurveyUtilTests(TestCase):

    def setUp(self):
        cleanup_db()

    def test_answer_not_required(self):

        survey_type = SurveyType(survey_template_id='test')
        survey_type.save()

        question = SurveyQuestion(survey_type=survey_type, question_id='optional_info', question_number=1, question_text='Any extra info?', valid_answers='.*', required_by='n')
        self.assertFalse(photo_survey.views.SurveyorView.is_answer_required(question, { "question_id": "optional_info", "answer": "" }), "is_answer_required() identifies optional answers")

    def test_avail_answer_question_id(self):

        survey_type = SurveyType(survey_template_id='test')
        survey_type.save()

        survey_question = SurveyQuestion(survey_type=survey_type, question_id='sample_question', question_number=1, question_text='Question Text')
        survey_question.save()

        avail_answer = SurveyQuestionAvailAnswer(survey_question=survey_question, value='value', text='Human readable question')
        avail_answer.save()

        self.assertEqual(avail_answer.survey_question_question_id(), survey_question.question_id)

    def test_survey_template_id(self):

        survey = create_survey()

        survey_type = SurveyType(survey_template_id='template_id')
        survey_type.save()

        survey_question = SurveyQuestion(survey_type=survey_type, question_id='qid', question_number=1, question_text='Question')
        survey_question.save()

        self.assertEqual(survey_question.survey_template_id, 'template_id')


class PhotoSurveyTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def get_auth_client(self):

        create_user()
        user = authenticate_user(email='lennon@thebeatles.com', password='johnpassword')

        token = Token.objects.create(user=user)
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # TODO do we absolutely need this?
        c.force_authenticate(user=user)

        return c

    def test_get_survey_count(self):
        c = Client()

        create_survey()

        response = c.get('/photo_survey/count/testparcelid/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({ "count": 1 }, response.data, "/photo_survey/count/<parce id>/ returns number of surveys available for the given parcel")

    def test_get_survey_metadata(self):

        c = Client()

        survey = create_survey('testparcelid')

        build_image_data('testparcelid')

        response = c.get('/photo_survey/testparcelid/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'images': ['http://testserver/data/photo_survey/images/demoimage1.jpg'], 'surveys': [survey.id], "publicly_owned": False}, response.data, "/photo_survey/<parce id>/ returns metadata about information available for the given parcel")

    def test_get_survey(self):

        c = Client()

        # Run a different test just to get a survey submitted
        self.test_post_survey_combined()

        survey = Survey.objects.first()

        expected = {'id': survey.id, 'image_url': '', 'note': '', 'created_at': date_json(survey.created_at), 'answers': [{'is_structure_on_site': 'y'}, {'is_structure_occupied': 'a'}, {'site_use_type': 'b'}, {'commercial_occupants_type': 'a'}, {'structure_condition': 'b'}, {'is_structure_fire_damaged': 'n'}, {'is_structure_secure': 'y'}, {'site_use': 'e'}, {'is_lot_maintained': 'y'}, {'is_dumping_on_site': 'n'}, {'blighted_lot_elements': 'a,b,c'}], 'status': '', 'common_name': '', 'parcel_id': 'testparcelid', 'surveyor': {'username': 'lennon@thebeatles.com', 'id': survey.user.id, 'email': 'lennon@thebeatles.com'}, 'survey_template': 'default_combined'}

        response = c.get("/photo_survey/survey/data/{}/".format(survey.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data, "/photo_survey/survey/data/<parce id>/ returns data from a survey")

    def test_get_latest_survey(self):

        c = Client()

        # Run a different test just to get a survey submitted
        self.test_post_survey_combined()

        survey = Survey.objects.first()

        expected = {'id': survey.id, 'image_url': '', 'note': '', 'created_at': date_json(survey.created_at), 'answers': [{'is_structure_on_site': 'y'}, {'is_structure_occupied': 'a'}, {'site_use_type': 'b'}, {'commercial_occupants_type': 'a'}, {'structure_condition': 'b'}, {'is_structure_fire_damaged': 'n'}, {'is_structure_secure': 'y'}, {'site_use': 'e'}, {'is_lot_maintained': 'y'}, {'is_dumping_on_site': 'n'}, {'blighted_lot_elements': 'a,b,c'}], 'status': '', 'common_name': '', 'parcel_id': 'testparcelid', 'surveyor': {'username': 'lennon@thebeatles.com', 'id': survey.user.id, 'email': 'lennon@thebeatles.com'}, 'survey_template': 'default_combined'}

        response = c.get("/photo_survey/survey/latest/testparcelid/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data, "/photo_survey/survey/latest/<parce id>/ returns data from latest survey for a parcel")

    def test_get_survey_404(self):

        c = Client()

        response = c.get("/photo_survey/survey/data/0000/")
        self.assertEqual(response.status_code, 404)

    def test_post_survey(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_default_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers")

    def test_post_survey_combined(self):

        build_survey_template_combined()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores combined field survey answers")
        self.assertEqual(response.data['parcel_survey_info'], { 'nearby_parcel_id': 0, 'testparcelid': 1 }, "/photo_survey/survey/ returns info about existing surveys")

    def test_post_survey_parcel_ok(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_lot_ok_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when lot does not need intervention")

    def test_post_survey_lot_bad(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_lot_bad_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when lot needs intervention")

    def test_post_survey_structure_bad(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_structure_bad_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers when structure needs intervention")

    def test_post_survey_invalid_parcel_id(self):

        build_survey_template_combined()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ stores combined field survey answers")
        self.assertEqual({'invalid parcel id': 'testparcelid'}, response.data, "Parcel id is identified as invalid")

    def test_post_survey_parcel_id_missing_meta(self):

        build_survey_template_combined()
        init_parcel_data()

        ParcelMetadata.objects.all().delete()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ handles parcels with no parcel metadata")

    def test_post_survey_unauthorized(self):

        build_survey_template_combined()
        init_parcel_data()

        c = Client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 401, "/photo_survey/survey/ requires authentication")

    def test_post_survey_json_auth_token(self):

        build_survey_template_combined()
        init_parcel_data()

        c = Client()
        create_user()
        user = authenticate_user(email='lennon@thebeatles.com', password='johnpassword')
        token = Token.objects.using('photo_survey').create(user=user)

        data = get_combined_survey_answers()
        data['auth_token'] = token.key

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ accepts auth token in json")

    def test_post_survey_not_secure(self):

        build_survey_template_combined()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_combined_survey_answers()), secure=False, content_type="application/json")
        self.assertEqual(response.status_code, 403, "/photo_survey/survey/ requires https")

    def test_post_survey_invalid_data(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][1]['answer'] = 'x'

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid data")
        self.assertEqual({'needs_intervention': 'question answer is invalid'}, response.data, "Parcel id is identified as invalid")

    def test_post_survey_missing_data(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'][0] = { "question_id": "parcel_id", "answer": "" }

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags missing data")
        self.assertEqual({'parcel_id': 'question answer is required'}, response.data, "Parcel id is identified as required")

    def test_invalid_survey_template(self):

        init_parcel_data()
        survey_answers = get_default_survey_answers()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid survey template")
        self.assertEqual({'invalid survey': 'default'}, response.data, "Parcel id is identified as required")

    def test_invalid_question_ids(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        survey_answers = get_default_survey_answers()
        survey_answers['answers'].append({ "question_id": "invalid", "answer": "" })

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(survey_answers), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 400, "/photo_survey/survey/ flags invalid survey template")
        self.assertEqual({'invalid question ids': ['invalid']}, response.data, "Parcel id is identified as required")

    def test_post_survey_structure_edgar(self):

        build_survey_template()
        init_parcel_data()

        c = self.get_auth_client()

        response = c.post('/photo_survey/survey/testparcelid/', json.dumps(get_edgars_survey_answers()), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/survey/ stores field survey answers from edgar")

    def test_status(self):

        # Run a different test just to get a survey submitted
        self.test_post_survey_combined()

        c = Client()

        response = c.get('/photo_survey/status/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({ 'testparcelid': 1 }, response.data, "/photo_survey/status/ returns how many times each parcel has been surveyed")

    def test_status_summary(self):

        # Run a different test just to get a survey submitted
        self.test_post_survey_combined()

        c = Client()

        response = c.get('/photo_survey/status/summary/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({ 'num_parcels_surveyed': 1 }, response.data, "/photo_survey/status/summary/ returns general information about surveys")

    def test_surveyor_survey_count(self):

        # Run a different test just to get a survey submitted
        self.test_post_survey_combined()

        c = Client()

        response = c.get('/photo_survey/surveyor/survey_count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'lennon@thebeatles.com': 1}], "/photo_survey/surveyor/survey_count/ returns count of surveys submitted by each surveyor")

    # TODO ideally this should be somewhere else since this is not testing an api call
    def test_survey_user(self):

        # Run a different test just to get a survey submitted
        self.test_post_survey_combined()

        survey = Survey.objects.first()
        self.assertEqual(survey.user.email, 'lennon@thebeatles.com')


def build_parcel_bridging_neighborhoods():
    parcel, created = ParcelMetadata.objects.get_or_create(parcel_id='testparcelid')
    parcel.save()

def build_survey_bridging_neighborhoods_template():

    survey_type = SurveyType(survey_template_id='bridging_neighborhoods')
    survey_type.save()

    data = [
        { "survey_type": survey_type, "question_id": "street_address", "question_number": 1,  "question_text": "What is the street address?", "valid_answers": ".*", "required_by": "", "required_by_answer": "" },
        { "survey_type": survey_type, "question_id": "node_id",        "question_number": 2,  "question_text": "What is the drupal node id?", "valid_answers": ".*", "required_by": "", "required_by_answer": "" },
        { "survey_type": survey_type, "question_id": "rating",         "question_number": 3,  "question_text": "What is the house rating?",   "valid_answers": "[0-4]", "required_by": "", "required_by_answer": "" },
    ]

    for row in data:
        template = SurveyQuestion(**row)
        template.save()

def get_bridging_neighborhoods_survey_answers():
    return {
        "username": "karlos",
        "answers": [
            {
                "question_id": "street_address",
                "answer": "1104 Military Street"
            },
            {
                "question_id": "node_id",
                "answer": "99"
            },
            {
                "question_id": "rating",
                "answer": "1"
            }
        ],
        "parcel_ids": ['testparcelid']
    }


class BridgingNeighborhoodsTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_user_likes_house(self):

        init_parcel_data()
        build_parcel_bridging_neighborhoods()
        build_survey_bridging_neighborhoods_template()

        data = get_bridging_neighborhoods_survey_answers()

        c = Client()

        response = c.post('/photo_survey/bridging_neighborhoods/favorites/testparcelid/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/bridging_neighborhoods/ stores resident's desired house")
        self.assertEqual(response.data['parcel_survey_info'], { 'testparcelid': 1 }, "/photo_survey/bridging_neighborhoods/ returns info about existing house surveys")
        self.assertEqual(User.objects.using('photo_survey').first().username, 'karlos')

    def test_existing_user_likes_house(self):

        init_parcel_data()
        build_parcel_bridging_neighborhoods()
        build_survey_bridging_neighborhoods_template()

        data = get_bridging_neighborhoods_survey_answers()

        c = Client()

        User.objects.db_manager('photo_survey').create_user("karlos").save()

        response = c.post('/photo_survey/bridging_neighborhoods/favorites/testparcelid/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201, "/photo_survey/bridging_neighborhoods/ stores resident's desired house")
        self.assertEqual(response.data['parcel_survey_info'], { 'testparcelid': 1 }, "/photo_survey/bridging_neighborhoods/ returns info about existing house surveys")
        self.assertEqual(User.objects.using('photo_survey').first().username, 'karlos')

    def test_user_likes_house_missing_username(self):

        init_parcel_data()
        build_parcel_bridging_neighborhoods()
        build_survey_bridging_neighborhoods_template()

        data = get_bridging_neighborhoods_survey_answers()
        del data['username']

        c = Client()

        response = c.post('/photo_survey/bridging_neighborhoods/favorites/testparcelid/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 401, "/photo_survey/bridging_neighborhoods/ requires username for resident")

    def test_get_user_likes(self):

        # run another test just to create a user and survey
        self.test_user_likes_house()

        c = Client()

        expected = {'favorites': {'testparcelid': {'node_id': '99', 'street_address': '1104 Military Street', 'rating': '1'}}}

        response = c.get('/photo_survey/bridging_neighborhoods/karlos/favorites/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data, "/photo_survey/bridging_neighborhoods/<username>/favorites/ returns current favorites for given user")

    def test_get_user_likes_not_secure(self):

        c = Client()

        response = c.get('/photo_survey/bridging_neighborhoods/karlos/favorites/', secure=False)
        self.assertEqual(response.status_code, 403)


    def test_get_user_likes_user_not_found(self):

        c = Client()

        response = c.get('/photo_survey/bridging_neighborhoods/invalid/favorites/', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_delete_user_like(self):

        # run another test just to create a user and survey
        self.test_user_likes_house()

        c = Client()

        response = c.delete('/photo_survey/bridging_neighborhoods/karlos/favorites/testparcelid/', secure=True)

        self.assertEqual(response.status_code, 204)
        favorites = Survey.objects.filter(survey_type__survey_template_id='bridging_neighborhoods').filter(parcel__parcel_id='testparcelid').exclude(status='deleted')
        self.assertFalse(favorites, "delete /photo_survey/<username>/bridging_neighborhoods/<parcelid> marks resident's desired house deleted")

    def test_delete_user_like_not_secure(self):

        c = Client()

        response = c.delete('/photo_survey/bridging_neighborhoods/karlos/favorites/testparcelid/', secure=False)
        self.assertEqual(response.status_code, 403)

    def test_delete_user_like_user_not_found(self):

        c = Client()

        response = c.delete('/photo_survey/bridging_neighborhoods/invalid/favorites/testparcelid/', secure=True)
        self.assertEqual(response.status_code, 404)


    def test_delete_user_like_not_found(self):

        # run another test just to create a user and survey
        self.test_user_likes_house()

        c = Client()

        response = c.delete('/photo_survey/bridging_neighborhoods/karlos/favorites/invalid/', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_user_changes_rating(self):

        # run another test just to create a user and survey
        self.test_user_likes_house()

        c = Client()

        data = get_bridging_neighborhoods_survey_answers()
        data['answers'][2]['answer'] = '2'

        response = c.post('/photo_survey/bridging_neighborhoods/favorites/testparcelid/', json.dumps(data), secure=True, content_type="application/json")
        self.assertEqual(response.status_code, 201)
