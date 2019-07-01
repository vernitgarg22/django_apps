import datetime

from django.db import models

from cod_utils.util import get_local_time


class LicensePlateInfo(models.Model):

    plate_num = models.CharField('License plate number', unique=True, db_index=True, max_length=16)
    created_at = models.DateTimeField('Date when plate number first added')

    def save(self, *args, **kwargs):

        # initialize created_at timestamp
        if self.created_at is None:
            self.created_at = get_local_time()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def __str__(self):
        return self.plate_num
