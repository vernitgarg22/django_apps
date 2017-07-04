import json
import re
import requests

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Count

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger

from photo_survey.models import Image, ImageMetadata
from photo_survey.models import Survey, SurveyQuestion, SurveyAnswer

from assessments.models import ParcelMaster


from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
def get_dummy_token(request):

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    if not request.is_secure():
        return Response({ "required must be secure": request.path }, status=status.HTTP_403_FORBIDDEN)

    # create a dummy user just to get a token
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    # return an auth token
    token = Token.objects.create(user=user)
    return Response({ "token": token.key }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def get_auth_token(request):

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    if not request.is_secure():
        return Response({ "required must be secure": request.path }, status=status.HTTP_403_FORBIDDEN)

    # Parse the data and get email and password
    data = json.loads(request.body.decode('utf-8'))
    if not data.get('email') or not data.get('password'):
        return Response({ "required": [ "email", "password" ] }, status=status.HTTP_400_BAD_REQUEST)

    email = data['email']
    password = data['password']

    # Try to authenticate the user
    # Note: we are using email for username
    user = authenticate(username=email, password=password)
    if not user:
        return Response({ "user not authorized": email }, status=status.HTTP_401_UNAUTHORIZED)

    # Authentication succeeded:  return an auth token
    token = Token.objects.create(user=user)
    return Response({ "token": token.key }, status=status.HTTP_201_CREATED)


# TODO remove this, if possible?
def clean_parcel_id(parcel_id):
    """
    Urls with dots are problematic: substitute underscores for dots in the url
    (and replace underscores with dots here)
    """
    return parcel_id.replace('_', '.')


@api_view(['GET'])
def get_survey_count(request, parcel_id):
    """
    Get number of images that exist currently for the given parcel.
    TODO: Clarify if we can identify a single survey, and return number of surveys available?
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_id = clean_parcel_id(parcel_id)

    image_metadata = ImageMetadata.objects.filter(parcel_id=parcel_id)
    content = { "count": len(image_metadata) }

    return Response(content)


@api_view(['GET'])
def get_metadata(request, parcel_id):
    """
    Get photos and survey data for the given parcel
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_id = clean_parcel_id(parcel_id)

    # TODO possibly optimize the images on the disk?
    # https://hugogiraudel.com/2013/07/29/optimizing-with-bash/
    # e.g., jpegtran -progressive image_raw.jpg small.jpg

    images = []
    image_metadata = ImageMetadata.objects.filter(parcel_id=parcel_id)
    for img_meta in image_metadata:
        url = request.build_absolute_uri(location='/data/photo_survey/images/' + img_meta.image.file_path)
        images.append(url)

    return Response({ "images": images })


def is_answer_required(question, answers):
    """
    Returns True if the answer is required
    """
    if question.required_by == 'n':
        return False
    if question.required_by and question.required_by_answer:
        previous_answer = answers.get(question.required_by, {}).get('answer')
        return previous_answer and re.fullmatch(question.required_by_answer, previous_answer)
    return True


def check_parcels(parcel_ids):

    survey_info = { parcel_id: 0 for parcel_id in parcel_ids }
    if parcel_ids:

        survey_counts = Survey.objects.filter(parcel_id__in=parcel_ids).annotate(count=Count('parcel_id'))
        for survey_count in survey_counts:
            survey_info[survey_count.parcel_id] = survey_count.count

    return survey_info


@api_view(['POST'])
def post_survey(request, parcel_id):
    """
    Post results of a field survey
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    if not request.user or not request.user.is_authenticated():
        return Response({ "error": "user not authorized" }, status=status.HTTP_401_UNAUTHORIZED)

    if not request.is_secure():
        return Response({ "error": "required must be secure" }, status=status.HTTP_403_FORBIDDEN)

    data = json.loads(request.body.decode('utf-8'))

    survey_template_id = data['survey_id']
    parcel_id = clean_parcel_id(parcel_id)
    answer_errors = {}

    # Is the parcel id valid?
    if not ParcelMaster.objects.filter(pnum__iexact=parcel_id).exists():
        return Response({ "invalid parcel id":  parcel_id }, status=status.HTTP_400_BAD_REQUEST)

    # What are our questions and answers?
    questions = SurveyQuestion.objects.filter(survey_template_id=survey_template_id).order_by('question_number')
    if not questions:
        return Response({ "invalid survey":  data['survey_id']}, status=status.HTTP_400_BAD_REQUEST)

    answers = { answer['question_id']: answer for answer in data['answers'] }

    # Report any answers that did not match a question_id
    question_ids = { question.question_id for question in questions }
    orphaned_answers = { key for key in answers.keys() if key not in question_ids }
    if orphaned_answers:
        return Response({ "invalid question ids": list(orphaned_answers) }, status=status.HTTP_400_BAD_REQUEST)

    # Validate each answer
    for question in questions:
        answer = answers.get(question.question_id)
        if answer and answer['answer']:
            if not question.is_valid(answer['answer']):
                answer_errors[question.question_id] = "question answer is invalid"
            elif question.answer_trigger and question.answer_trigger_action:
                # TODO clean this up - add 'skip to question' feature
                if re.fullmatch(question.answer_trigger, answer['answer']) and question.answer_trigger_action == 'exit':
                    break
        elif is_answer_required(question, answers):
            answer_errors[question.question_id] = "question answer is required"

    # Report invalid content?
    if answer_errors:
        return Response(answer_errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO:  add in common_name, note and status
    survey = Survey(survey_template_id=survey_template_id, user_id=data['user_id'], parcel_id=parcel_id,
                common_name=data.get('common_name', ''), note=data.get('note', ''), status=data.get('status', ''), image_url=data.get('image_url', ''))
    survey.save()

    # Save all the answers
    for answer in (a for a in answers.values() if a['answer']):
        answer = SurveyAnswer(**answer)
        answer.survey = survey
        answer.save()

    # Indicate number of surveys present for each parcel id in the request
    parcel_info = check_parcels(data.get('parcel_ids', []))

    return Response({ "answers": answers, "parcel_survey_info": parcel_info }, status=status.HTTP_201_CREATED)


#
# TODO:
#
# - add ability to return survey answers
# 