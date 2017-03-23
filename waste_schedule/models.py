import requests
from datetime import date

from django.db import models
from waste_wizard.models import WasteItem
from django.core.exceptions import ValidationError
from django.core import validators
from django.core.validators import validate_comma_separated_integer_list


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


class ScheduleDetail(models.Model):

    SERVICE_TYPE_CHOICES = (('all', 'All Services'),) + WasteItem.DESTINATION_CHOICES

    CHANGE_CHOICES = (
        ('schedule', 'Schedule Change'),
        ('start-date', 'Service Start Date'),
        ('end-date', 'Service End Date'),
        ('info', 'Notification'),
    )

    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    GIS_URL = "https://gis.detroitmi.gov/arcgis/rest/services/Services/services/MapServer/0/query?where=day+%3D%27{0}%27&returnIdsOnly=true&f=json"

    detail_type = models.CharField('Type of information', max_length = 128, choices=CHANGE_CHOICES)
    service_type = models.CharField('Service', max_length=32, choices=SERVICE_TYPE_CHOICES, default=SERVICE_TYPE_CHOICES[0][0])
    description = models.CharField('Description of change', max_length = 256)
    normal_day = models.DateField('Normal day of service', db_index=True, null=True, blank=True)
    new_day = models.DateField('Rescheduled day of service', db_index=True, null=True, blank=True)
    note = models.CharField('Note', max_length = 256, null=True, blank=True)
    waste_area_ids = models.CharField('Waste area(s) effected', max_length = 1028, null=True, blank=True, validators=[validate_comma_separated_integer_list])

    def __str__(self):
        return self.detail_type + " - " + self.description

    def clean(self):
        if self.waste_area_ids is None and self.normal_day is None:
            raise ValidationError({'normal_day': "If waste area(s) are not set then normal day must be set"})

        if self.detail_type == 'info':
            if self.new_day is not None:
                raise ValidationError({'new_day': 'Information alerts should not change scheduled services'})
        elif self.detail_type == 'schedule':
            if self.new_day is None:
                raise ValidationError({'new_day': 'Please schedule a new service date'})
            if self.normal_day is None:
                raise ValidationError({'normal_day': 'Please indicate the regular service date'})
        elif self.detail_type == 'start-date' or self.detail_type == 'end-date':
            if self.new_day is None:
                raise ValidationError({'new_day': 'Please indicate the relevant date'})
        else:
            raise ValidationError({'new_day': "Invalid change type " + self.detail_type})

    def save(self, *args, **kwargs):

        if not self.waste_area_ids and self.detail_type == 'schedule':
            self.waste_area_ids = self.find_waste_areas(self.normal_day)

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    @staticmethod
    def find_waste_areas(date):

        # build url to get all waste areas for this day of week
        weekday_str = ScheduleDetail.DAYS[date.weekday()]
        url = ScheduleDetail.GIS_URL.format(weekday_str)

        # request the data and parse it
        r = requests.get(url)
        id_list = [ str(id) +',' for id in r.json()['objectIds'] or [] ]
        ids = ''.join(id_list)
        if ids.endswith(','):
            ids = ids[0: len(ids) - 1]
        return ids

# 
# from waste_schedule.models import ScheduleDetail
# ch = ScheduleDetail(detail_type='schedule', description='test', normal_day='2017-7-4', new_day='2017-7-4')
#
# Change pickup in certain areas due to holiday
# ch = ScheduleDetail(detail_type='schedule', normal_day='2017-07-04', new_day='2017-07-05', description='Due to 4th of July holiday, pickup postponed by one day', waste_area_ids='1,4,6')
#
# Display information telling all customers about an upcoming wayne county drop-off day
# ch = ScheduleDetail(detail_type='info', normal_day='2017-07-16', description='Wayne County drop-off day')
#
# Reschedule service for specific area(s) due to an emergency 
# ch = ScheduleDetail(detail_type='schedule', normal_day='2017-03-21', new_day='2017-03-22', description='Customers affected by flooding from the recent water main break on Jefferso Avenue will have waste pickup delayed by one day', waste_area_ids='2,3')
#
