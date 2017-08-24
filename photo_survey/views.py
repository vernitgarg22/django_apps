import json
import re
import requests

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Count

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from cod_utils.cod_logger import CODLogger

from photo_survey.models import Image, ImageMetadata
from photo_survey.models import ParcelMetadata, SurveyType, Survey, SurveyQuestion, SurveyAnswer
from photo_survey.models import PublicPropertyData

from assessments.models import ParcelMaster

from cod_utils.util import date_json


def get_survey_data(survey):
    answers = [ { survey_answer.question_id: survey_answer.answer } for survey_answer in survey.surveyanswer_set.all() ]
    return {
        "id": survey.id,
        "survey_template": survey.survey_template_id,
        "parcel_id": survey.parcel.parcel_id,
        "created_at": date_json(survey.created_at),
        "surveyor": {
            "id": survey.user.id,
            "username": survey.user.username,
            "email": survey.user.email,
        },
        "answers": answers,
        "common_name": survey.common_name,
        "note": survey.note,
        "image_url": survey.image_url,
        "status": survey.status,
    }


def authenticate_user(email, password, using = 'photo_survey'):
    """
    Returns True if user
    """

    try:
        user = User.objects.db_manager(using).get_by_natural_key(email)
    except User.DoesNotExist:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a nonexistent user (#20760).
        User().set_password(password)
    else:
        if user and user.check_password(password) and user.is_active:
            return user


@api_view(['POST'])
def get_auth_token(request):

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    if not request.body or request.body == b'{}':
        return Response({ "required": [ "email", "password" ] }, status=status.HTTP_400_BAD_REQUEST)

    # Parse the data and get email and password
    data = json.loads(request.body.decode('utf-8'))
    if not data.get('email') or not data.get('password'):
        return Response({ "required": [ "email", "password" ] }, status=status.HTTP_400_BAD_REQUEST)

    email = data['email']
    password = data['password']

    # Try to authenticate the user
    # Note: we are using email for username
    user = authenticate_user(email, password)
    if not user:
        return Response({ "user not authorized": email }, status=status.HTTP_401_UNAUTHORIZED)

    # Authentication succeeded:  return an auth token
    token, created = Token.objects.using('photo_survey').get_or_create(user=user)
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
    Get number of surveys that exist currently for the given parcel.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_id = clean_parcel_id(parcel_id)

    count = Survey.objects.filter(parcel__parcel_id=parcel_id).count()
    content = { "count": count }

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
    image_metadata = ImageMetadata.objects.filter(parcel__parcel_id=parcel_id)
    for img_meta in image_metadata:
        url = request.build_absolute_uri(location='/data/photo_survey/images/' + img_meta.image.file_path)
        images.append(url)

    surveys = [ survey.id for survey in Survey.objects.filter(parcel__parcel_id=parcel_id) ]

    # Is this parcel publicly owned?
    # TODO: make sure the dataset for this eventually 'goes live' (currently we load it
    # whenever dexter slusarski gets a new csv with this content)
    public_property_data = PublicPropertyData.objects.filter(parcelno=parcel_id)
    publicly_owned = len(public_property_data) > 0

    return Response({ "images": images, "surveys": surveys, "publicly_owned": publicly_owned })


@api_view(['GET'])
def get_survey(request, survey_id):
    """
    Get photos and survey data for the given parcel
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    surveys = Survey.objects.filter(id=int(survey_id))
    if not surveys:
         return Response({"survey not found": survey_id}, status=status.HTTP_404_NOT_FOUND)

    return Response(get_survey_data(surveys[0]))


@api_view(['GET'])
def get_latest_survey(request, parcel_id):
    """
    Returns latest survey data for the parcel.
    TODO return latest survey that has a 'good' status.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_id = clean_parcel_id(parcel_id)

    survey = Survey.objects.filter(parcel__parcel_id=parcel_id).last()

    content = get_survey_data(survey) if survey else {}

    return Response(content)


class SurveyorView(APIView):

    @staticmethod
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

    def get_surveyor(self, request, data):
        """
        Return the user to associate with the survey.
        """

        user = None
        if request.user and request.user.is_authenticated():
            user = request.user
        else:
            # TODO remove this once we get mod_wsgi passing the authorization header through properly
            buf = data.get("auth_token", "")
            tokens = Token.objects.using("photo_survey").filter(key=buf)
            if tokens:
                user = tokens[0].user

        return user

    def get_survey_template_id(self, data):
        """
        Return survey template id - identifies the survey type to use.
        """

        return data['survey_id']

    def check_parcels(self, parcel_ids):
        """
        Returns json mapping each parcel_id to number of surveys that exist currently for that parcel.
        """

        survey_info = { parcel_id: 0 for parcel_id in parcel_ids }
        if parcel_ids:

            survey_counts = ParcelMetadata.objects.filter(parcel_id__in=parcel_ids).annotate(count=Count('survey'))
            for survey_count in survey_counts:
                survey_info[survey_count.parcel_id] = survey_count.count

        return survey_info

    def post(self, request, parcel_id, format=None):
        """
        Post results of a field survey
        """

        CODLogger.instance().log_api_call(name=__name__, msg=request.path)

        if not request.is_secure():
            return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)



        # TODO remove this once we get mod_wsgi passing the authorization header through properly
        auth_meta = request.META.get('HTTP_AUTHORIZATION')
        if auth_meta:
            print(auth_meta)
        else:
            print('saw no http auth meta')



        data = json.loads(request.body.decode('utf-8'))

        # What user is posting this?
        user = self.get_surveyor(request, data)

        if user == None:
            return Response({ "error": "user not authorized" }, status=status.HTTP_401_UNAUTHORIZED)

        survey_template_id = self.get_survey_template_id(data)
        parcel_id = clean_parcel_id(parcel_id)
        answer_errors = {}

        # Is the parcel id valid?
        if not ParcelMaster.objects.filter(pnum__iexact=parcel_id).exists():
            return Response({ "invalid parcel id":  parcel_id }, status=status.HTTP_400_BAD_REQUEST)

        # What are our questions and answers?
        questions = SurveyQuestion.objects.filter(survey_type__survey_template_id=survey_template_id).order_by('question_number')
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
            if answer and answer.get('answer'):
                if not question.is_valid(answer['answer']):
                    answer_errors[question.question_id] = "question answer is invalid"
                elif question.answer_trigger and question.answer_trigger_action:
                    # TODO clean this up - add 'skip to question' feature
                    if re.fullmatch(question.answer_trigger, answer['answer']) and question.answer_trigger_action == 'exit':
                        break
            elif SurveyorView.is_answer_required(question, answers):
                answer_errors[question.question_id] = "question answer is required"

        # Report invalid content?
        if answer_errors:
            return Response(answer_errors, status=status.HTTP_400_BAD_REQUEST)

        parcel = ParcelMetadata.objects.get(parcel_id=parcel_id)

        # Create the survey
        survey_type = SurveyType.objects.get(survey_template_id=survey_template_id)
        survey = Survey(survey_type=survey_type, user_id=str(user.id), parcel=parcel,
                    common_name=data.get('common_name', ''), note=data.get('note', ''), status=data.get('status', ''), image_url=data.get('image_url', ''))
        survey.save()

        # Save all the answers
        for survey_question in questions:
            answer = answers.get(survey_question.question_id)
            if answer and answer['answer']:
                survey_answer = SurveyAnswer(survey=survey, survey_question=survey_question, answer=answer['answer'], note=answer.get('answer', None))
                survey_answer.save()

        # Indicate number of surveys present for each parcel id in the request
        parcel_info = self.check_parcels(data.get('parcel_ids', []))

        return Response({ "answers": answers, "parcel_survey_info": parcel_info }, status=status.HTTP_201_CREATED)


class BridgingNeighborhoodsView(SurveyorView):

    def get_surveyor(self, request, data):
        """
        Return the bridging neighborhoods resident to associate with the survey.
        """

        user = None
        if not data.get('username'):
            return None

        user = User.objects.db_manager('photo_survey').create_user(data['username'])
        user.save()

        return user

    def get_survey_template_id(self, data):
        """
        Return the one and only survey template id for bridging neighborhoods.
        """

        return "bridging_neighborhoods"

    def describe_favorite(self, survey):
        """
        Returns dict of information about this survey.
        """

        return { survey_answer.survey_question.question_id : survey_answer.answer for survey_answer in survey.survey_answers }

    def get(self, request, username, format=None):
        """
        Returns list of parcels (houses) a resident is interested in.
        """

        CODLogger.instance().log_api_call(name=__name__, msg=request.path)

        if not request.is_secure():
            return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.using('photo_survey').filter(username = username)
        if not users:
            return Response({"User not found": username}, status=status.HTTP_404_NOT_FOUND)

        surveys = Survey.objects.filter(user_id = users[0].id)
        favorites = { survey.parcel.parcel_id : self.describe_favorite(survey) for survey in surveys }

        return Response({ "favorites": favorites })


@api_view(['GET'])
def get_status(request):
    """
    Returns all parcels that have already been surveyed.  Each parcel is paired with the number of
    times it has been surveyed.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    parcel_counts = ParcelMetadata.objects.all().annotate(count=Count('survey'))
    content = { parcel_count.parcel_id : parcel_count.count for parcel_count in parcel_counts }

    return Response(content)


@api_view(['GET'])
def get_status_summary(request):
    """
    Returns general info:  number of parcels that currently have surveys, etc.
    TODO:  add any other metadata here?
    e.g., add in this, but for residential / commercial:
    num_parcels_total = ParcelMaster.objects.count()
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    num_parcels_surveyed = Survey.objects.values('parcel_id').distinct().count()

    return Response({ "num_parcels_surveyed": num_parcels_surveyed })


@api_view(['GET'])
def get_surveyor_survey_count(request):
    """
    Returns number of surveys each surveyor has completed.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    user_info = { user.id : user for user in User.objects.using('photo_survey') }
    survey_counts = Survey.objects.values('user_id').annotate(count=Count('parcel_id', distinct=True)).order_by('-count')

    results = []
    for survey_count in survey_counts:
        user = user_info[int(survey_count['user_id'])]
        results.append({ user.email : survey_count['count'] })

    return Response(results)
