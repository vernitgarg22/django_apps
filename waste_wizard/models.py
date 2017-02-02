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
    destination = models.CharField('Appropriate waste destination', max_length=32, choices=DESTINATION_CHOICES)
    notes = models.CharField('Special details to note', max_length=300, blank=True)
    keywords = models.CharField('Keywords associated with the item', max_length=300, default='', blank=True)
    def __str__(self):
        return self.description + ' (' + self.destination + ')'
    def urlsafe(self):
        return urllib.parse.quote(self.description)


# TODO:
# - add image url

# wi = WasteItem(description='', destination='', notes='', keywords='')
