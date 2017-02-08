import urllib.parse
from django.db import models


class WasteItem(models.Model):
    DESTINATION_CHOICES = (
        ('trash', 'Trash'),
        ('recycling', 'Recycling'),
        ('bulk', 'Bulk'),
        ('yard waste', 'Yard Waste'),
        ('compost', 'Compost'),
    )

    app_label = 'waste_wizard'
    description = models.CharField('Waste item description', max_length=200, unique=True, db_index=True)
    destination = models.CharField('Correct destination', max_length=32, choices=DESTINATION_CHOICES)
    notes = models.CharField('Special details to note (optional)', max_length=300, blank=True)
    keywords = models.CharField('Associated keywords (optional)', max_length=300, default='', blank=True)
    image_url = models.CharField('Associated image (optional)', max_length=100, default='', blank=True)
    def __str__(self):
        return self.description + ' (' + self.destination + ')'
