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


# TODO: rename this to "SurveyAnswer?"
class SurveyData(models.Model):
    """
    Stores field survey answers.
    """

    app_label = 'photo_survey'

    user_id = models.CharField('User ID', max_length=64, unique=False, db_index=True)
    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)
    question_id = models.CharField('Question identifier', max_length=64)
    answer = models.CharField("Answer", max_length=1024)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return "user: " + self.user_id + \
            " survey: " + self.survey_template_id + \
            " question: " + self.question_id + \
            " answer: " + self.answer


# TODO: rename this to "SurveyQuestion?"
class SurveyTemplate(models.Model):
    """
    Defines different types of surveys.
    """

    app_label = 'photo_survey'

    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)
    question_id = models.CharField('Question identifier', max_length=64)
    question_number = models.PositiveIntegerField('Question number', unique=False)
    question_text = models.CharField('Question', max_length=256, unique=False, help_text='The actual human-readable question itself')

    # TODO rename valid_answers?
    valid_answers = models.CharField('Valid answers', max_length=256, unique=False, help_text="Pipe-delimited list of valid answers ('*' = anything)")

    required_by = models.CharField('Required by', max_length=64, null=True, blank=True, unique=False, help_text='Question / Answer pair that makes this required')
    required_by_answer = models.CharField('Required by answer', max_length=64, null=True, blank=True, unique=False, help_text='Specific Answer pattern that makes this required')

    def is_valid(self, answer):
        """
        Return True if answer is valid
        TODO check if is_xyz() is correct method name?
        """

        return answer and re.fullmatch(self.valid_answers, answer)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return "survey: " + self.survey_template_id + \
            " question: " + self.question_id + \
            " " + str(self.question_number) + \
            " " + self.question_text + \
            " (valid answers: " + self.valid_answers + ")"


class ImageMetadata(models.Model):
    """
    Contains information about a specific image.
    """

    app_label = 'photo_survey'

    parcel_id = models.CharField('Path to image file', max_length=32, unique=False, db_index=True)
    image = models.ForeignKey(Image)
    created_at = models.DateTimeField('Time when image was created')
    # TODO: get lat/long/altitude working
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
    # altitude = models.DecimalField(max_digits=6, decimal_places=3, blank=True)
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


# TODO:  Should we bother to have this class as well?
# class Parcel(models.Model):
#     app_label = 'photo_survey'
