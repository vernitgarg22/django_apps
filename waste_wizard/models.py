import urllib.parse
from django.db import models


class WasteItem(models.Model):
    DESTINATION_CHOICES = (
        ('bulk', 'Bulk'),
        ('hazardous', 'Hazardous Waste'),
        ('recycling', 'Recycling'),
        ('recycle here', 'Recycle Here'),
        ('trash', 'Trash'),
        ('transfer station', 'Transfer Station'),
        ('yard waste', 'Yard Waste'),
    )

    IMAGE_CHOICES = (
        ('bulk.png', 'Bulk'),
        ('recycle_here.jpg', 'Recycle Here'),
        ('recycling.png', 'Recycling'),
        ('trash.png', 'Trash'),
        ('yard_waste.png', 'Yard Waste'),
    )

    DESTINATION_NOTES = {
        "recycle here": "Recycle Here Recycling Center"
    }

    app_label = 'waste_wizard'
    description = models.CharField('Waste item description', max_length=200, unique=True, db_index=True)
    destination = models.CharField('Correct destination', max_length=32, choices=DESTINATION_CHOICES)
    notes = models.CharField('Special details to note (optional)', max_length=300, blank=True)
    keywords = models.CharField('Associated keywords (optional)', max_length=300, default='', blank=True)
    image_url = models.CharField('Associated image (optional)', max_length=100, default='', blank=True, choices=IMAGE_CHOICES)
    def __str__(self):
        return self.description + ' (' + self.destination + ')'

    def  get_destination(self):
        return self.DESTINATION_NOTES.get(self.destination, self.destination.title())


# class Destination(models.Model):
#     SCHEDULE_CHOICES = (
#         ('weekly', 'Weekly'),
#         ('biweekly', 'Bi-Weekly'),
#     )

#     name = models.CharField('Destination name', max_length=32, unique=True, db_index=True, choices=WasteItem.DESTINATION_CHOICES)
#     schedule = models.CharField('Schedule', max_length=32, choices=SCHEDULE_CHOICES)


# class WasteArea(models.Model):
#     description = models.CharField('Waste area description', max_length=128, unique=True, db_index=True)
