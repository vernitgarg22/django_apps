import re

from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_comma_separated_integer_list


class Subscriber(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    DEFAULT_STATUS=STATUS_CHOICES[1][0]
    ACTIVE_STATUS=STATUS_CHOICES[0][0]
    VALID_CHOICE_VALUES = [ t[0] for t in STATUS_CHOICES ]

    phone_number = models.CharField('Subscriber phone number', unique = True, max_length = 32)
    waste_area_ids = models.CharField('Subscriber Waste area(s)', max_length = 64, validators=[validate_comma_separated_integer_list])
    status = models.CharField('Subscriber status (for soft deletes)', max_length = 32, choices=STATUS_CHOICES, default=DEFAULT_STATUS)

    def __str__(self):
        return self.phone_number + ' - ' + self.waste_area_ids + ' - ' + self.status

    def clean(self):

        # validate phone number format (must be 10 digits)
        if not (re.search(r'^\d{10}$', self.phone_number)):
            raise ValidationError({'phone_number': "Phone number must be 10 digits"})

        if not len(self.waste_area_ids):
            raise ValidationError({'waste_area_ids': "Waste area ids value is required"})

        if not self.waste_area_ids.endswith(','):
            self.waste_area_ids = self.waste_area_ids + ','

        # validate waste area ids is comma-delimited list of integer, ending in a comma
        if not (re.search(r'^[\d,]+,$', self.waste_area_ids)):
            raise ValidationError({'waste_area_ids': "Waste area ids must be comma-delimited list of integers, ending in a comma"})

        # only certain values are allowed for status
        if not self.VALID_CHOICE_VALUES.count(self.status):
            raise ValidationError({'status': "Status must be one of " + str(self.VALID_CHOICE_VALUES)})

    def activate(self):
        """
        Marks subscriber active, then validates and saves
        """
        self.status = Subscriber.ACTIVE_STATUS
        self.clean()
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

        # validate and save subscriber
        subscriber.clean()
        subscriber.save()

        return subscriber, None