import requests
from datetime import date
from enum import Enum

from django.db import models
from waste_wizard.models import WasteItem
from django.core.exceptions import ValidationError
from django.core import validators
from django.core.validators import validate_comma_separated_integer_list


class BiWeekType(Enum):
    A = 'a'
    B = 'b'

    @staticmethod
    def from_str(ch):
        for week_type in BiWeekType:
            if ch == week_type.value:
                return week_type
        raise Exception('invalid week type value')


class ScheduleDetail(models.Model):

    SERVICE_TYPE_CHOICES = (('all', 'All Services'),) + WasteItem.DESTINATION_CHOICES

    TYPE_CHOICES = (
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

    DEFAULT_SERVICE_TYPE = SERVICE_TYPE_CHOICES[0][0]
    SERVICES_LIST = ''.join([ val[0] + ', ' for val in SERVICE_TYPE_CHOICES ])[:-2]

    GIS_URL = "https://gis.detroitmi.gov/arcgis/rest/services/DPW/DPW_Services/MapServer/{0}/query?where=day+%3D%27{1}%27&spatialRel=esriSpatialRelIntersects&outFields=FID,week,contractor&returnDistinctValues=false&f=json"

    app_label = 'waste_schedule'
    detail_type = models.CharField('Type of information', max_length = 128, choices=TYPE_CHOICES)
    service_type = models.CharField('Service', max_length=32, default=DEFAULT_SERVICE_TYPE, help_text="(comma-delimited combination of any of the following: " + SERVICES_LIST + ')')
    description = models.CharField('Description of change', max_length = 256)
    normal_day = models.DateField('Normal day of service', db_index=True, null=True, blank=True)
    new_day = models.DateField('Rescheduled day of service', db_index=True, null=True, blank=True)
    note = models.CharField('Note', max_length = 256, null=True, blank=True)
    waste_area_ids = models.CharField('Waste area(s) effected', max_length = 1028, null=True, blank=True, validators=[validate_comma_separated_integer_list])

    @property
    def sort_value(self):
        return (self.normal_day if self.normal_day else self.new_day)

    def __str__(self):
        return 'type: ' + self.detail_type + " - description: " + self.description + ' - routes: ' + self.waste_area_ids

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
        if not ScheduleDetail.is_valid_service_type(self.service_type):
            raise ValidationError({'service_type': "Invalid service type: " + self.service_type})

    def save(self, *args, **kwargs):

        # if admin did not specify waste area ids, look them up for trash service
        # and add in recycling & bulk to the detail note so the admin will know about any
        # conflicts with recycling or bulk pickup
        if not self.waste_area_ids and self.detail_type == 'schedule':
            self.waste_area_ids = self.get_waste_route_ids(self.normal_day)

            recycling_ids = self.get_waste_route_ids(self.normal_day, ScheduleDetail.RECYCLING)
            bulk_ids = self.get_waste_route_ids(self.normal_day, ScheduleDetail.BULK)

            self.note = self.note + "{0} (other service conflicts: recycling for {1} and bulk/hazardous/yard waste for {2})".format(self.note or '', recycling_ids, bulk_ids)

        # force waste_area_ids to start and end with ','
        if not self.waste_area_ids.startswith(','):
            self.waste_area_ids = ',' + self.waste_area_ids

        if not self.waste_area_ids.endswith(','):
            self.waste_area_ids = self.waste_area_ids + ','

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    @staticmethod
    def is_valid_service_type(service_type):
        """
        Returns true if each comma-separated value in the service_type string is valid
        """
        service_map = { val[0]: val[1] for val in ScheduleDetail.SERVICE_TYPE_CHOICES }
        for type_val in service_type.split(','):
            if type_val and not service_map.get(type_val):
                return False
        return True

    @staticmethod
    def check_date_service(date, week_type):
        if week_type == BiWeekType.A:
            return date.year % 2 != date.isocalendar()[1] % 2
        else:
            return date.year % 2 == date.isocalendar()[1] % 2

    @staticmethod
    def get_waste_routes(date, service_type = TRASH):
        """
        Returns dictionary mapping route ids to week type ('a' or 'b')
        pertaining to routes getting serviced on the particular date
        """

        weekday_str = ScheduleDetail.DAYS[date.weekday()]

        # get the gis id of the service
        service_id = ScheduleDetail.SERVICE_ID_MAP[service_type]

        # build url to get all waste areas for service and this day of week
        url = ScheduleDetail.GIS_URL.format(service_id, weekday_str)

        # retrieve data and parse out a map of route ids (FIDs) and A or B weeks
        r = requests.get(url)
        routes = { feature['attributes']['FID']: feature['attributes']['week'] for feature in r.json()['features'] }

        # only return routes that are affected by current week
        # (Note: trash is every week)
        if service_type != ScheduleDetail.TRASH:
            routes = { route_id: routes[route_id] for route_id in list(routes.keys()) if ScheduleDetail.check_date_service(date, BiWeekType.from_str(routes[route_id])) }

        return routes

    @staticmethod
    def get_waste_route_ids(date, service_type = TRASH):
        """
        Returns comma-delimited list of route ids
        pertaining to routes getting serviced on the particular date
        """

        routes = ScheduleDetail.get_waste_routes(date, service_type)
        return ',' + ''.join( [ str(route_id) + ',' for route_id in list(routes.keys()) ] )

    @staticmethod
    def get_schedule_changes(route_id, date):
        return ScheduleDetail.objects.using('default').filter(waste_area_ids__contains=',8,').filter(normal_day__exact=date)
