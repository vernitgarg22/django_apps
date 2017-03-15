from django.db import models
from waste_wizard.models import WasteItem
from django.core.exceptions import ValidationError


class WasteArea(models.Model):

    ALL_WASTE_AREAS_ID = 1000

    description = models.CharField('Waste area description', max_length=128, unique=True, db_index=True)
    order_val = models.IntegerField('Waste area ordering value', null=True)
    def __str__(self):
        "Returns waste area's full description, including waste area id"
        if self.id == self.ALL_WASTE_AREAS_ID:
            return str(self.description)
        else:
            return str(self.id) + ' - ' + self.description

    class Meta:
        ordering = ['order_val']


class ScheduleChange(models.Model):
    app_label = 'waste_schedule'

    SERVICE_TYPE_CHOICES = (('all', 'All Services'),) + WasteItem.DESTINATION_CHOICES

    service_type = models.CharField('Service', max_length=32, choices=SERVICE_TYPE_CHOICES, default=SERVICE_TYPE_CHOICES[0][0])
    waste_area = models.ForeignKey('waste_schedule.WasteArea', on_delete=models.DO_NOTHING)
    normal_day = models.DateField('Normal day of service', db_index=True)
    rescheduled_day = models.DateField('New day of service', db_index=True)
    reason = models.CharField('Reason for change', max_length=300, blank=True)
    note = models.CharField('Special note for residents', max_length=300, blank=True)
    def __str__(self):
        return self.service_type + \
            ' changed from ' + str(self.normal_day) + \
            ' to ' + str(self.rescheduled_day) + \
            ' because ' + self.reason + \
            ' - ' + self.note

    def clean(self):
        if self.rescheduled_day <= self.normal_day:
            raise ValidationError({'rescheduled_day': 'Rescheduled day must be after normally scheduled day'})
