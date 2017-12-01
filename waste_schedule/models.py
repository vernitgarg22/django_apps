import re
import requests
from enum import Enum

from django.db import models
from django.core.exceptions import ValidationError

from waste_wizard.models import WasteItem
from cod_utils import util


class BiWeekType(Enum):
    A = 'a'
    B = 'b'

    @staticmethod
    def from_str(ch):
        for week_type in BiWeekType:
            if ch == week_type.value:
                return week_type
        raise Exception('invalid week type value')

    def __str__(self):
        return self.value


class ScheduleDetail(models.Model):

    app_label = 'waste_schedule'

    ALL = 'all'
    RECYCLING = WasteItem.DESTINATION_CHOICES[2][0]
    BULK = WasteItem.DESTINATION_CHOICES[0][0]
    TRASH = WasteItem.DESTINATION_CHOICES[5][0]
    YARD_WASTE = WasteItem.DESTINATION_CHOICES[7][0]

    YEAR_ROUND_SERVICES = [ TRASH, RECYCLING, BULK ]

    SERVICE_TYPE_CHOICES = ((ALL, 'All Services'),) + WasteItem.DESTINATION_CHOICES

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

    SERVICE_ID_MAP = {
        RECYCLING: 0,
        BULK: 1,
        TRASH: 2,
    }

    DEFAULT_SERVICE_TYPE = SERVICE_TYPE_CHOICES[0][0]
    SERVICES_LIST = ''.join([ val[0] + ', ' for val in SERVICE_TYPE_CHOICES ])[:-2]

    GIS_URL_ALL = "https://gis.detroitmi.gov/arcgis/rest/services/DPW/All_Services/MapServer/0/query?where=1%3D1&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&outSR=4326&f=json"
    GIS_URL_DAY = "https://gis.detroitmi.gov/arcgis/rest/services/DPW/All_Services/MapServer/0/query?where=day+%3D%27{0}%27&1%3D1&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&outSR=4326&f=json"

    app_label = 'waste_schedule'
    detail_type = models.CharField('Type of information', max_length = 128, choices=TYPE_CHOICES)
    service_type = models.CharField('Service', max_length=32, default=DEFAULT_SERVICE_TYPE, help_text="(comma-delimited combination of any of the following: " + SERVICES_LIST + ')')
    description = models.CharField('Description of change', max_length=512)
    normal_day = models.DateField('Normal day of service', db_index=True, null=True, blank=True)
    new_day = models.DateField('Rescheduled day of service', db_index=True, null=True, blank=True)
    note = models.CharField('Note', max_length = 256, null=True, blank=True)
    waste_area_ids = models.CharField('Waste area(s) effected', max_length = 1028, null=True, blank=True)

    @property
    def sort_value(self):
        return (self.normal_day if self.normal_day else self.new_day)

    def __str__(self):
        return 'type: ' + self.detail_type + " - " + self.service_type + " - description: " + self.description + ' - routes: ' + self.waste_area_ids

    def json(self):
        return {
            "type": self.detail_type,
            "service": self.service_type,
            "description": self.description,
            "normalDay": util.date_json(self.normal_day),
            "newDay": util.date_json(self.new_day),
            "note": self.note,
            "wasteAreaIds": self.waste_area_ids,
        }

    def clean(self):

        # validate the waste area ids (but allow empty string)
        if self.waste_area_ids and not (re.search(r'^[0-9,][0-9,]*$', self.waste_area_ids)):
            raise ValidationError({'waste_area_ids': "Must be comma-separated list of numbers"})

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

        # TODO clear this up
        if kwargs.get('null_waste_area_ids'):
            self.waste_area_ids = None
            del kwargs['null_waste_area_ids']

        # clean up waste_area_ids
        self.waste_area_ids = util.clean_comma_delimited_string(self.waste_area_ids)

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    @staticmethod
    def is_valid_service_type(service_type):
        """
        Returns true if each comma-separated value in the service_type string is valid
        """

        service_type = service_type.strip()
        if not service_type:
            return False

        service_map = { val[0]: val[1] for val in ScheduleDetail.SERVICE_TYPE_CHOICES }
        for type_val in service_type.split(','):
            if type_val and not service_map.get(type_val):
                return False
        return True

    @staticmethod
    def get_date_week_type(date):
        """
        Returns type of week ('a' or 'b') that the given date belongs to.
        """

        year_is_even = (date.year % 2 == 0)
        week_is_even = (date.isocalendar()[1] % 2 == 0)
        return BiWeekType.B if year_is_even == week_is_even else BiWeekType.A

    @staticmethod
    def check_date_service(date, week_type):
        """
        Returns true if a service with the given week_type will happen 
        on the same week as 'date'
        """

        return ScheduleDetail.get_date_week_type(date) == week_type

    # TODO might want to move some of these static methods to a util file

    @staticmethod
    def is_same_service_type(ours, theirs):
        """
        Returns True if the 2 service types are the same.  In particular:
        - if theirs or ours is 'all', returns True
        - if theirs is 'recycle' and ours is 'recycling' returns True
        """
        if ScheduleDetail.ALL in [ours, theirs]:
            return True
        if ours == ScheduleDetail.RECYCLING:
            return theirs == 'recycle'
        else:
            return ours == theirs

    @staticmethod
    def get_waste_routes(date, service_type = TRASH):
        """
        Returns dictionary mapping route ids to week type ('a' or 'b')
        pertaining to routes getting serviced on the particular date
        """
        weekday_str = ScheduleDetail.DAYS[date.weekday()]

        # build url to get all waste areas for this day of week
        url = ScheduleDetail.GIS_URL_DAY.format(weekday_str)

        # retrieve data and parse out a map of route ids (FIDs) and A or B weeks
        r = requests.get(url)

        # features = [ feature for feature in r.json()['features'] ]
        features = [ feature for feature in r.json()['features'] if ScheduleDetail.is_same_service_type(service_type, feature['attributes']['services']) ]

        routes = { feature['attributes']['FID']: feature['attributes']['week'] for feature in features }

        # only return routes that are affected by current week
        # (Note: trash is every week)
        if service_type != ScheduleDetail.TRASH:
            routes = { route_id: routes[route_id] for route_id in list(routes.keys()) if ScheduleDetail.check_date_service(date, BiWeekType.from_str(routes[route_id])) }

        return routes

    @staticmethod
    def get_schedule_changes(route_id, date):
        """
        Returns schedule details pertaining to the given route and date
        """

        details = ScheduleDetail.objects.filter(waste_area_ids__contains="," + str(route_id) + ",").filter(normal_day__exact=date)
        return details.filter(normal_day__exact=date) | details.filter(new_day__exact=date)
