from datetime import datetime

from django.db import models
from django.utils import timezone


class ElectionNotification(models.Model):

    app_label = 'elections'

    NOTIFICATION_CHOICES = (
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    )

    notification_type = models.CharField('Notification type', max_length=32, choices=NOTIFICATION_CHOICES, default='reminder')
    day = models.DateField('Day on which notification should be sent')
    message = models.CharField('Notification message', max_length=512, blank=True, null=True)

    # TODO figure out how to do geocoding - add a set of precincts?


class ElectionSubscriber(models.Model):

    app_label = 'elections'

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    phone_number = models.CharField('Subscriber phone number', unique=True, max_length=32)
    status = models.CharField('Subscriber status', max_length=32, choices=STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField('Time of initial subscription', default=timezone.now())
    last_status_update = models.DateTimeField('Time of last status change', default=timezone.now())
    latitude = models.CharField('Latitude', max_length=32)
    longitude = models.CharField('Longitude', max_length=32)
    address = models.CharField('Home address', max_length=128)
