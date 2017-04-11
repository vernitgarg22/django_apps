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

    def __str__(self):
        return self.phone_number + ' - routes: ' + self.waste_area_ids + ' - status: ' + self.status + ' - services: ' + self.service_type

    def clean(self):

        # validate phone number format (must be 10 digits)
        if not (re.search(r'^\d{10}$', self.phone_number)):
            raise ValidationError({'phone_number': "Phone number must be 10 digits"})

        if not len(self.waste_area_ids):
            raise ValidationError({'waste_area_ids': "Waste area ids value is required"})

        # validate the waste area ids
        validators.validate_comma_separated_integer_list(self.waste_area_ids)

        # only certain values are allowed for status
        if not self.VALID_STATUS_VALUES.count(self.status):
            raise ValidationError({'status': "Status must be one of " + str(self.VALID_STATUS_VALUES)})

        # validate each comma-delimited value in service_type
        if not ScheduleDetail.is_valid_service_type(self.service_type):
            raise ValidationError({'service_type': "Invalid service type: " + self.service_type})

    def save(self, *args, **kwargs):

        # clean up waste_area_ids
        self.waste_area_ids = util.clean_comma_delimited_string(self.waste_area_ids)

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)


    def activate(self):
        """
        Marks subscriber active, then validates and saves
        """
        self.status = Subscriber.ACTIVE_STATUS
        self.clean()
        self.save()

    def deactivate(self):
        """
        Marks subscriber active, then validates and saves
        """
        self.status = Subscriber.INACTIVE_STATUS
        self.clean()
        self.save()

    def delete(self, using=None, keep_parents=False):
        """
        Do a soft-delete (i.e., set status to 'inactive')
        """
        self.status = Subscriber.INACTIVE_STATUS
        self.save()

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

        if data.get("service_type"):
            subscriber.service_type = data['service_type']

        # validate and save subscriber
        subscriber.clean()
        subscriber.save()

        return subscriber, None