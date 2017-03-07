import urllib.parse
from django.db import models


class WasteItem(models.Model):
    DESTINATION_CHOICES = (
        ('bulk', 'Bulk'),
        ('drop off', 'Recycle Here'),
        ('hazardous', 'Hazardous Waste'),
        ('recycling', 'Recycling'),
        ('trash', 'Trash'),
        ('transfer station', 'Transfer Station'),
        ('yard waste', 'Yard Waste'),
    )

    IMAGE_CHOICES = (
        ('bulk.png', 'Bulk'),
        ('recycling.png', 'Recycling'),
        ('trash.png', 'Trash'),
        ('yard_waste.png', 'Yard Waste'),
    )

    app_label = 'waste_wizard'
    description = models.CharField('Waste item description', max_length=200, unique=True, db_index=True)
    destination = models.CharField('Correct destination', max_length=32, choices=DESTINATION_CHOICES)
    notes = models.CharField('Special details to note (optional)', max_length=300, blank=True)
    keywords = models.CharField('Associated keywords (optional)', max_length=300, default='', blank=True)
    image_url = models.CharField('Associated image (optional)', max_length=100, default='', blank=True, choices=IMAGE_CHOICES)
    def __str__(self):
        return self.description + ' (' + self.destination + ')'

# TODO start using this
class Destination(models.Model):
    DESTINATION_CHOICES = (
        ('bulk', 'Bulk'),
        ('drop off', 'Recycle Here'),
        ('hazardous', 'Hazardous Waste'),
        ('recycling', 'Recycling'),
        ('trash', 'Trash'),
        ('transfer station', 'Transfer Station'),
        ('yard waste', 'Yard Waste'),
    )

    SCHEDULE_CHOICES = (
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-Weekly'),
    )

    name = models.CharField('Destination name', max_length=32, unique=True, db_index=True, choices=DESTINATION_CHOICES)
    schedule = models.CharField('Schedule', max_length=32, db_index=True, choices=SCHEDULE_CHOICES)
    date_start = models.DateField('Next service start date', null=True)
    date_end = models.DateField('Next service end date', null=True)