import base64
import json
import re
import requests

from django.conf import settings
from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger

from photo_survey.models import Image, ImageMetadata, SurveyTemplate, SurveyData


# TODO remove this, if possible?
def clean_parcel_id(parcel_id):
    """
    Urls with dots are problematic: substitute underscores for dots in the url
    (and replace underscores with dots here)
    """
    return parcel_id.replace('_', '.')


def encode_image_filename(filename):
    filename = filename.replace('/', '_')
    return filename[0:-4]


def decode_image_filename(filename):
    filename = filename.replace('_', '/')
    return filename + ".jpg"


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

    images = []
    image_metadata = ImageMetadata.objects.filter(parcel_id=parcel_id)
    for img_meta in image_metadata:
        images.append(encode_image_filename(img_meta.image.file_path))

    return Response({ "images": images })


@api_view(['GET'])
def get_image(request, image_path):
    """
    Return the given photo as base64-encoded string
    (note: when decoding the data you should first remove the quotes at the beginning and end of the string.)
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    data = None
    full_path = settings.AUTO_LOADED_DATA["PHOTO_SURVEY_IMAGE_PATH"] + decode_image_filename(image_path)

    try:
        with open(full_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError as error:
        raise Http404("File not found")

    return Response(base64.b64encode(data))


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


@api_view(['POST'])
def post_survey(request, parcel_id):
    """
    Post results of a field survey
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_id = clean_parcel_id(parcel_id)
    data = json.loads(request.body.decode('utf-8'))
    answer_errors = {}

    # What are our questions and answers?
    questions = SurveyTemplate.objects.filter(survey_template_id=data['survey_id']).order_by('question_number')
    if not questions:
        return Response("Invalid survey template id: " + str(data['survey_id']), status=status.HTTP_400_BAD_REQUEST)

    answers = { answer['question_id']: answer for answer in data['answers'] }

    # Report any answers that did not match a question_id
    keys = { question.question_id for question in questions }
    orphaned_answers = [ answer for answer in answers.values() if answer['question_id'] not in keys ]
    if orphaned_answers:
        return Response({ "invalid question ids": orphaned_answers }, status=status.HTTP_400_BAD_REQUEST)

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

    # Save all the answers
    for answer in (a for a in answers.values() if a['answer']):
        answer['parcel_id'] = parcel_id
        SurveyData(**answer).save()

    # TODO verify that at least 1 answer got saved?

    return Response({ "answers": answers }, status=status.HTTP_201_CREATED)


#
# TODO:
#
# - add ability to return survey answers
# 