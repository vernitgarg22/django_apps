import datetime
import re

from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_comma_separated_integer_list

from waste_schedule.models import ScheduleDetail
from cod_utils import util


class Subscriber(models.Model):

    ACTIVE_STATUS = 'active'
    INACTIVE_STATUS = 'inactive'
    STATUS_CHOICES = (
        (ACTIVE_STATUS, 'Active'),
        (INACTIVE_STATUS, 'Inactive'),
    )
    DEFAULT_STATUS=INACTIVE_STATUS
    VALID_STATUS_VALUES = [ ACTIVE_STATUS, INACTIVE_STATUS ]

    phone_number = models.CharField('Subscriber phone number', unique = True, max_length = 32)
    waste_area_ids = models.CharField('Subscriber Waste area(s)', max_length = 64, validators=[validate_comma_separated_integer_list])
    status = models.CharField('Subscriber status (for soft deletes)', max_length = 32, choices=STATUS_CHOICES, default=DEFAULT_STATUS)
    service_type = models.CharField('Service', max_length=32, default=ScheduleDetail.DEFAULT_SERVICE_TYPE, help_text="(comma-delimited combination of any of the following: " + ScheduleDetail.SERVICES_LIST + ')')
    last_status_update = models.DateTimeField('Time of last status change', blank=True, null=True)
    created_at = models.DateTimeField('Time of initial subscription', blank=True, null=True)
    comment = models.CharField('Internal use only', max_length = 128, blank=True, null=True)
    latitude = models.CharField('Latitude', max_length = 32, blank=True, null=True)
    longitude = models.CharField('Longitude', max_length = 32, blank=True, null=True)
    address = models.CharField('Home address', max_length = 128, blank=True, null=True)

    def __str__(self):
        string = self.phone_number + ' - routes: ' + self.waste_area_ids + ' - status: ' + self.status + ' - services: ' + self.service_type
        if self.comment:
            string = string + " (" + self.comment + ")"
        return string

    def clean(self):

        # validate phone number format (must be 10 digits)
        if not (re.search(r'^\d{10}$', self.phone_number)):
            raise ValidationError({'phone_number': "Phone number must be 10 digits"})

        if not self.waste_area_ids:
            raise ValidationError({'waste_area_ids': "Waste area ids value is required"})

        # validate the waste area ids
        validators.validate_comma_separated_integer_list(self.waste_area_ids)

        # only certain values are allowed for status
        if self.status not in self.VALID_STATUS_VALUES:
            raise ValidationError({'status': "Status must be one of " + str(self.VALID_STATUS_VALUES)})

        # validate each comma-delimited value in service_type
        if not ScheduleDetail.is_valid_service_type(self.service_type):
            raise ValidationError({'service_type': "Invalid service type: " + self.service_type})

    def save(self, *args, **kwargs):

        # clean up waste_area_ids
        self.waste_area_ids = util.clean_comma_delimited_string(self.waste_area_ids)

        # initialize created_at timestamp
        if self.created_at is None:
            self.created_at = util.get_local_time()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def change_status(self, activate):
        """
        Internal use only:  changes status to active or inactive and
        updates last_status_update to current time.
        """
        self.status = Subscriber.ACTIVE_STATUS if activate else Subscriber.INACTIVE_STATUS
        self.last_status_update = util.get_local_time()
        self.clean()
        self.save()

    def activate(self):
        """
        Marks subscriber active, then validates and saves
        """
        self.change_status(True)

    def deactivate(self):
        """
        Marks subscriber inactive, then validates and saves
        """
        self.change_status(False)

    def delete(self, using=None, keep_parents=False):
        """
        Do a soft-delete (i.e., set status to 'inactive')
        """
        self.deactivate()

    @staticmethod
    def update_or_create_from_dict(data):
        """
        Using dictionary of form data, update existing subscriber or create new one
        """

        if not data.get('phone_number') or not data.get('waste_area_ids'):
            # TODO replace this with error 403 or something like that
            return None, {"error": "phone_number and waste_area_ids are required"}

        phone_number = data['phone_number']

        # update existing subscriber or create new one
        subscriber = Subscriber.objects.none()
        previous = Subscriber.objects.filter(phone_number__exact=phone_number)
        if previous.exists():
            subscriber = previous[0]
            subscriber.phone_number=phone_number
            subscriber.waste_area_ids=data['waste_area_ids']
            subscriber.status=Subscriber.DEFAULT_STATUS
        else:
            # try to create a subscriber with the posted data
            subscriber = Subscriber(phone_number=phone_number, waste_area_ids=data['waste_area_ids'])

        # set service type
        if data.get("waste_service_type"):
            subscriber.service_type = data['waste_service_type'].replace('|', ',')

        # check for optional values
        for value in [ 'address', 'latitude', 'longitude' ]:
            if data.get(value):
                setattr(subscriber, value, data.get(value))

        # validate and save subscriber
        subscriber.clean()
        subscriber.save()

        return subscriber, None