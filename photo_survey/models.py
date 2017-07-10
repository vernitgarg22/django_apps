from datetime import datetime
import re

from django.db import models


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

    parcel_id = models.CharField('Path to image file', max_length=32, unique=False, db_index=True)
    image = models.ForeignKey(Image)
    created_at = models.DateTimeField('Time when image was created')
    latitude = models.FloatField('Image latitude')
    longitude = models.FloatField('Image longitude')
    altitude = models.FloatField('Image altitude')
    house_number = models.IntegerField('House number', unique=False, null=True, blank=True)
    street_name = models.CharField('Street name', max_length=128, null=True, blank=True, unique=False)
    street_type = models.CharField('Street type', max_length=32, null=True, blank=True, unique=False)
    zipcode = models.CharField('zipcode', max_length=16, blank=True, null=True, unique=False)
    common_name = models.CharField('Common name', max_length=128, null=True, blank=True, unique=False)
    note = models.CharField('Image note', max_length=128, null=True, blank=True)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        desc = str(self.image)
        desc = desc + ' - created at: ' + self.created_at.strftime("%Y-%m-%d %H:%M")
        if self.note:
            desc = desc + ' - note: ' + self.note
        return desc


class Survey(models.Model):
    """
    Stores a survey's survey for a given parcel
    """

    app_label = 'photo_survey'

    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)
    user_id = models.CharField('User ID', max_length=64, unique=False, db_index=True)
    parcel_id = models.CharField('Parcel id', max_length=32, unique=False, db_index=True)
    created_at = models.DateTimeField('Time when survey was made', null=True, default=None)
    common_name = models.CharField("Parcel common name", max_length=1024)
    note = models.CharField("Note", max_length=1024)
    image_url = models.CharField("Image used for survey", max_length=256)
    status = models.CharField('Survey status', max_length=16, blank=True, unique=False, db_index=True)

    def save(self, *args, **kwargs):
        """
        Override save() method so we can set created_at
        """

        self.created_at = datetime.now()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)


    # TODO finish this
    # def get_survey_answers(self, parcel_id):
    #     """
    #     Returns answes belonging to the survey, for the given parcel id
    #     """

    #     return self.survey_ansers

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


class SurveyAnswer(models.Model):
    """
    Stores field survey answers.
    """

    app_label = 'photo_survey'

    survey = models.ForeignKey(Survey)
    question_id = models.CharField('Question identifier', max_length=64)
    answer = models.CharField("Answer", max_length=1024)
    note = models.CharField("Note", max_length=1024, blank=True, unique=False)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        desc = " survey: " + self.survey_template_id + \
            " question: " + self.question_id + \
            " answer: " + self.answer
        if self.note:
            desc = desc + " note: " + self.note
        return desc


class SurveyQuestion(models.Model):
    """
    Defines different types of survey questions
    """

    app_label = 'photo_survey'

    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)
    question_id = models.CharField('Question identifier', max_length=64)
    question_number = models.PositiveIntegerField('Question number', unique=False)
    question_text = models.CharField('Question', max_length=256, unique=False, help_text='The actual human-readable question itself')

    # TODO rename valid_answers?
    valid_answers = models.CharField('Valid answers', max_length=256, unique=False, help_text="Pipe-delimited list of valid answers ('*' = anything)")

    required_by = models.CharField('Required by', max_length=64, blank=True, default='', unique=False, help_text="Question / Answer pair that makes answer required. 'n' makes answer optional. Default is required")
    required_by_answer = models.CharField('Required by answer', max_length=64, blank=True, default='', unique=False, help_text='Specific answer pattern that makes this required')
    answer_trigger = models.CharField('Answer trigger', max_length=16, blank=True, default='', unique=False, help_text="Required action for a given answer. e.g., 'n'")
    answer_trigger_action = models.CharField('Trigger action', max_length=16, blank=True, default='', unique=False, help_text="Action to take if a trigger goes off. e.g., 'stop'")

    def is_valid(self, answer):
        """
        Return True if answer is valid
        TODO check if is_xyz() is correct method name?
        TODO move this to the answer class
        """

        return answer and re.fullmatch(self.valid_answers, answer)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return "survey: " + self.survey_template_id + \
            " question: " + self.question_id + \
            " " + str(self.question_number) + \
            " " + self.question_text + \
            " (valid answers: " + self.valid_answers + ")"
