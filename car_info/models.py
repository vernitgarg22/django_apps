from datetime import datetime

from django.db import models
from django.utils import timezone

from cod_utils.util import date_json


class LicensePlateInfo(models.Model):

    plate_num = models.CharField('License plate number', unique=True, db_index=True, max_length=16)
    created_at = models.DateTimeField('Date when plate number first added')

    def save(self, *args, **kwargs):

        # initialize created_at timestamp
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def __str__(self):    # pragma: no cover (this is mostly just for debugging)
        return "plate: " + self.plate_num + " created_at: " + str(date_json(self.created_at))
