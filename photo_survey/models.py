from django.db import models


class Image(models.Model):
    """
    Contains information required to retrieve an image.
    """

    app_label = 'photo_survey'

    file_path = models.CharField('Path to image file', max_length=256, unique=True, db_index=True)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        return self.file_path


class SurveyTemplate(models.Model):
    """
    Defines different types of surveys.
    """

    app_label = 'photo_survey'

    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)
    user_id = models.CharField('User ID', max_length=64, unique=False, db_index=True)
    question_id = models.CharField('Question identifier', max_length=64)
    question_number = models.PositiveIntegerField('Question number', unique=False)
    question_text = models.CharField('Question', max_length=256, unique=False, help_text='The actual human-readable question itself')
    valid_answers = models.CharField('Valid answers', max_length=256, unique=False, help_text="Pipe-delimited list of valid answers ('*' = anything)")


class SurveyData(models.Model):
    """
    Stores field survey answers.
    """

    app_label = 'photo_survey'

    survey_template_id = models.CharField('Survey name or ID', max_length=32, unique=False, db_index=True)
    question_id = models.CharField('Question identifier', max_length=64)
    answer = models.CharField("Answer", max_length=1024)


class ImageMetadata(models.Model):
    """
    Contains information about a specific image.
    """

    app_label = 'photo_survey'

    parcel_id = models.CharField('Path to image file', max_length=32, unique=False, db_index=True)
    created_at = models.DateTimeField('Time when image was added')
    note = models.CharField('Image note', max_length=128, blank=True)
    image = models.ForeignKey(Image)

    def __str__(self):    # pragma: no cover  (this is really just for debugging)
        desc = str(self.image)
        desc = desc + ' - created at: ' + self.created_at.strftime("%Y-%m-%d %H:%M")
        if self.note:
            desc = desc + ' - note: ' + self.note
        return desc


# TODO:  Should we bother to have this class as well?
# class Parcel(models.Model):
#     app_label = 'photo_survey'
