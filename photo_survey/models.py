from django.db import models


class Image(models.Model):
    """
    Contains information required to retrieve an image
    """

    app_label = 'photo_survey'

    file_path = models.CharField('Path to image file', max_length=256, unique=True, db_index=True)

    def __str__(self):
        return self.file_path


class ImageMetadata(models.Model):
    """
    Contains information about a specific image
    """

    app_label = 'photo_survey'

    parcel_id = models.CharField('Path to image file', max_length=32, unique=False, db_index=True)
    created_at = models.DateTimeField('Time when image was added')
    note = models.CharField('Image note', max_length=128, blank=True)
    image = models.ForeignKey(Image)

    def __str__(self):
        desc = str(self.image)
        desc = desc + ' - created at: ' + self.created_at.strftime("%Y-%m-%d %H:%M")
        if self.note:
            desc = desc + ' - note: ' + self.note
        return desc


# TODO:  Should we bother to have this class as well?
# class Parcel(models.Model):
#     app_label = 'photo_survey'


# from photo_survey.models import Image, ImageMetadata
# from datetime import datetime
# img = Image(file_path='foobar.jpg')
# img_meta = ImageMetadata(image=img, parcel_id='parcel_id', created_at=datetime.now(), note='test image')
