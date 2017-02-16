from django.db import models
from waste_wizard.models import WasteItem
from django.core.exceptions import ValidationError


class ScheduleException(models.Model):
    app_label = 'waste_schedule'

    SERVICE_TYPE_CHOICES = (('all', 'All Services'),) + WasteItem.DESTINATION_CHOICES

    # TODO Add in waste area id

    service_type = models.CharField('Service', max_length=32, choices=SERVICE_TYPE_CHOICES, default=SERVICE_TYPE_CHOICES[0][0])
    normal_day = models.DateField('Normal day of service', db_index=True)
    rescheduled_day = models.DateField('New day of service', db_index=True)
    reason = models.CharField('Reason for change', max_length=300, blank=True)
    note = models.CharField('Special note for residents', max_length=300, blank=True)

    def clean(self):
        if self.rescheduled_day <= self.normal_day:
            raise ValidationError({'rescheduled_day': 'Rescheduled day must be after normally scheduled day'})
