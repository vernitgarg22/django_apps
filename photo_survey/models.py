import re

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ParcelMetadata(models.Model):
    """
    Parcel-related data (mainly to connect various surveys and images together).
    """

    parcel_id = models.CharField('Parcel ID', max_length=32, unique=True, db_index=True)
    common_name = models.CharField('Common name', max_length=128, null=True, blank=True, unique=False)
    house_number = models.IntegerField('House number', unique=False, null=True, blank=True)
    street_name = models.CharField('Street name', max_length=128, null=True, blank=True, unique=False)
    street_type = models.CharField('Street type', max_length=32, null=True, blank=True, unique=False)
    zipcode = models.CharField('zipcode', max_length=16, blank=True, null=True, unique=False)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return self.parcel_id


class SurveyType(models.Model):
    """
    Groups together a set of survey questions.
    """

    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return self.survey_template_id


class Survey(models.Model):
    """
    Stores a surveyors's survey answers for a given parcel.
    """

    app_label = 'photo_survey'

    survey_type = models.ForeignKey(SurveyType, on_delete=models.PROTECT)
    user_id = models.CharField('User ID', max_length=64, unique=False, db_index=True)
    parcel = models.ForeignKey(ParcelMetadata, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Time when survey was made', null=True, default=None)
    common_name = models.CharField("Parcel common name", max_length=1024)
    note = models.CharField("Note", max_length=1024)
    image_url = models.CharField("Image used for survey", max_length=256)
    status = models.CharField('Survey status', max_length=16, blank=True, unique=False, db_index=True)

    @property
    def survey_template_id(self):
        return self.survey_type.survey_template_id

    @property
    def parcel_id(self):
        return self.parcel.parcel_id

    @property
    def user(self):
        """
        Return the surveyor (user) who created the survey
        """

        return User.objects.using('photo_survey').filter(id=self.user_id).first()

    def save(self, *args, **kwargs):
        """
        Override save() method so we can set created_at
        """

        self.created_at = timezone.now()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    @property
    def survey_questions(self):
        """
        Returns the questions belonging to the survey.
        TODO: remove this method and use ForeignKey()
        """

        return SurveyQuestion.objects.filter(survey_template_id=self.survey_template_id).order_by('question_number')

    # @property
    # def survey_answers(self):
    #     """
    #     Returns the answers belonging to the survey.
    #     TODO: remove this method and use ForeignKey()
    #     """

    #     questions = self.survey_questions

    #     answers_dict = { answer.question_id : answer for answer in SurveyAnswer.objects.filter(survey_id=self.id) }

    #     answers = []
    #     for question in questions:
    #         answer = answers_dict.get(question.question_id)
    #         if answer:
    #             answers.append(answer)

    #     return answers

    ordering = ['survey_template_id', 'parcel_id', 'common_name', 'status']

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        desc = "user: " + self.user_id + \
            " survey: " + self.survey_template_id
        if self.common_name:
            desc = desc + " common name: " + self.common_name
        if self.note:
            desc = desc + " note: " + self.note
        if self.status:
            desc = desc + " status: " + self.status
        return desc


class SurveyQuestion(models.Model):
    """
    Defines different types of survey questions.
    """

    app_label = 'photo_survey'

    survey_type = models.ForeignKey(SurveyType, on_delete=models.PROTECT)
    question_id = models.CharField('Question identifier', max_length=64)
    question_number = models.PositiveIntegerField('Question number', unique=False)
    question_text = models.CharField('Question', max_length=256, unique=False, help_text='The actual human-readable question itself')
    valid_answers = models.CharField('Valid answers regex', max_length=256, unique=False, help_text="Regex defining valid answers")
    required_by = models.CharField('Required by', max_length=64, blank=True, default='', unique=False, help_text="Question / Answer pair that makes answer required. 'n' makes answer optional. Default is required")
    required_by_answer = models.CharField('Required by answer', max_length=64, blank=True, default='', unique=False, help_text='Specific answer pattern that makes this required')
    answer_trigger = models.CharField('Answer trigger', max_length=16, blank=True, default='', unique=False, help_text="Required action for a given answer. e.g., 'n'")
    answer_trigger_action = models.CharField('Trigger action', max_length=16, blank=True, default='', unique=False, help_text="Action to take if a trigger goes off. e.g., 'stop'")
    scoring_type = models.CharField('Way to score the answers for the question', max_length=16, blank=True, default='', unique=False)

    @property
    def survey_template_id(self):
        return survey_type.survey_template_id

    ordering = ['survey_template_id', 'question_number']

    def is_valid(self, answer):
        """
        Return True if answer is valid
        TODO check if is_xyz() is correct method name?
        TODO move this to the answer class
        """

        return answer and re.fullmatch(self.valid_answers, answer)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return "survey: " + self.survey_type.survey_template_id + \
            " question: " + self.question_id + \
            " " + str(self.question_number) + \
            " " + self.question_text + \
            " (valid answers: " + self.valid_answers + ")"


class SurveyQuestionAvailAnswer(models.Model):
    """
    Defines different answers available for each question.
    """

    app_label = 'photo_survey'

    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT)
    value = models.CharField('Answer Value', max_length=64, unique=False, help_text="Answer value as stored in database")
    text = models.CharField('Human-readable Answer', max_length=128, unique=False, help_text="Human-readable version of answer")
    weight = models.IntegerField('Answer Weight', unique=False, default=0)

    def survey_question_question_id(self):
        return self.survey_question.question_id

    survey_question_question_id.short_description = 'Survey Question ID'

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return self.survey_question.question_id + ' - ' + self.value + ' - ' + self.text


class SurveyAnswer(models.Model):
    """
    Stores field survey answers.
    """

    app_label = 'photo_survey'

    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT)
    answer = models.CharField("Answer", max_length=1024)
    note = models.CharField("Note", max_length=1024, blank=True, unique=False)

    @property
    def question_id(self):
        return self.survey_question.question_id

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        desc = " survey: " + str(self.survey.survey_template_id) + \
            " question: " + self.survey_question.question_id + \
            " answer: " + self.answer
        if self.note:
            desc = desc + " note: " + self.note
        return desc


class Image(models.Model):
    """
    Contains information required to retrieve an image.
    """

    app_label = 'photo_survey'

    file_path = models.CharField('Path to image file', max_length=256, unique=True, db_index=True)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return self.file_path


class ImageMetadata(models.Model):
    """
    Contains information about a specific image.
    """

    app_label = 'photo_survey'

    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    parcel = models.ForeignKey(ParcelMetadata, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Time when image was created')
    latitude = models.FloatField('Image latitude')
    longitude = models.FloatField('Image longitude')
    altitude = models.FloatField('Image altitude')
    note = models.CharField('Image note (optional)', max_length=128, null=True, blank=True)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        desc = str(self.image)
        desc = desc + ' - created at: ' + self.created_at.strftime("%Y-%m-%d %H:%M")
        if self.note:
            desc = desc + ' - note: ' + self.note
        return desc


class PublicPropertyData(models.Model):
    """
    Defines information about known public property.
    Note:  this table was provided as a one-off csv file from Dexter Slusarski and
    should be updated as often as possible.  Ideally it should be replaced
    with live data.
    """

    # TODO where should this live?
    app_label = 'photo_survey'

    parcelno = models.CharField('Parcel ID', max_length=32, db_index=True)
    propaddress = models.CharField('Address', max_length=64)
    propzip = models.CharField('ZIP', max_length=12)
    taxpayer1 = models.CharField('Tax Payer 1', max_length=64)
    taxpayer2 = models.CharField('Tax Payer 2', max_length=64)
    taxaddr = models.CharField('Tax Payer Address', max_length=64)
    taxcity = models.CharField('Tax Payer City', max_length=32)
    taxstate = models.CharField('Tax Payer State', max_length=2)
    taxzip = models.CharField('Tax Payer ZIP', max_length=32)
    project_co = models.CharField('Project Code', max_length=32)
    ownership = models.CharField('Owner', max_length=64)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return self.parcelno + ' - ' + self.propaddress + ' - ' + self.taxpayer1 + ' - ' + self.ownership
