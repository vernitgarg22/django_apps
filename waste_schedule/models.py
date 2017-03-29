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
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    RECYCLING = WasteItem.DESTINATION_CHOICES[2][0]
    BULK = WasteItem.DESTINATION_CHOICES[0][0]
    TRASH = WasteItem.DESTINATION_CHOICES[4][0]

    SERVICE_ID_MAP = {
        RECYCLING: 0,
        BULK: 1,
        TRASH: 2,
    }

    SERVICES_LIST = ''.join([ val[0] + ', ' for val in SERVICE_TYPE_CHOICES ])[:-2]

    GIS_URL = "https://gis.detroitmi.gov/arcgis/rest/services/DPW/DPW_Services/MapServer/{0}/query?where=day+%3D%27{1}%27&returnIdsOnly=true&f=json"

    detail_type = models.CharField('Type of information', max_length = 128, choices=CHANGE_CHOICES)
    service_type = models.CharField('Service', max_length=32, default=SERVICE_TYPE_CHOICES[0][0], help_text="(comma-delimited combination of any of the following: " + SERVICES_LIST + ')')
    description = models.CharField('Description of change', max_length = 256)
    normal_day = models.DateField('Normal day of service', db_index=True, null=True, blank=True)
    new_day = models.DateField('Rescheduled day of service', db_index=True, null=True, blank=True)
    note = models.CharField('Note', max_length = 256, null=True, blank=True)
    waste_area_ids = models.CharField('Waste area(s) effected', max_length = 1028, null=True, blank=True, validators=[validate_comma_separated_integer_list])

    @property
    def sort_value(self):
        return (self.normal_day if self.normal_day else self.new_day)

    def __str__(self):
        return self.detail_type + " - " + self.description

    def json(self):
        return {
            "type": self.detail_type,
            "service": self.service_type,
            "description": self.description,
            "normalDay": self.normal_day,
            "newDay": self.new_day,
            "note": self.note,
            "wasteAreaIds": self.waste_area_ids,
        }

    def clean(self):

        # every detail must have either a normal date or a new date (required for sorting)
        if not self.normal_day and not self.new_day:
            raise ValidationError({'normal_day': "Must have either a normal date or a new date"})

        # if schedule change, then either waste_area_ids or normal_day must be provided
        if self.detail_type == 'schedule' and not self.waste_area_ids and not self.normal_day:
            raise ValidationError({'normal_day': "For schedule change, if waste area(s) are not set then normal day must be set"})

        # perform validations related to detail_type
        if not self.detail_type:
            raise ValidationError({'detail_type': 'Detail type is required'})
        elif self.detail_type == 'info':
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
            raise ValidationError({'detail_type': "Invalid detail type: " + self.detail_type})

        # validate the different comma-separated values in the service_type string
        service_map = { val[0]: val[1] for val in self.SERVICE_TYPE_CHOICES }
        for type_val in self.service_type.split(','):
            if not service_map.get(type_val):
                raise ValidationError({'service_type': "Invalid service type: " + type_val})

    def save(self, *args, **kwargs):

        # if admin did not specify waste area ids, look them up for trash service
        # and add in recycling & bulk to the detail note so the admin will know about any
        # conflicts with recycling or bulk pickup
        if not self.waste_area_ids and self.detail_type == 'schedule':
            self.waste_area_ids = self.find_waste_areas(self.normal_day)
            recycling_ids = self.find_waste_areas(self.normal_day, ScheduleDetail.RECYCLING)
            bulk_ids = self.find_waste_areas(self.normal_day, ScheduleDetail.BULK)

            self.note = self.note + "{0} (other service conflicts: recycling for {1} and bulk/hazardous/yard waste for {2})".format(self.note or '', recycling_ids, bulk_ids)

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    @staticmethod
    def find_waste_areas(date, service_type = TRASH):

        weekday_str = ScheduleDetail.DAYS[date.weekday()]

        # get the gis id of the service
        service_id = ScheduleDetail.SERVICE_ID_MAP[service_type]

        # build url to get all waste areas for service and this day of week
        url = ScheduleDetail.GIS_URL.format(service_id, weekday_str)

        # request the data and parse it
        r = requests.get(url)
        id_list = [ str(id) +',' for id in r.json()['objectIds'] or [] ]
        return ''.join(id_list)
