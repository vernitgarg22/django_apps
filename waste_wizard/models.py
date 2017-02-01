import urllib.parse
from django.db import models


class WasteItem(models.Model):
    app_label = 'waste_wizard'
    description = models.CharField('Waste item description', max_length=200)
    destination = models.CharField('Appropriate waste destination', max_length=32)
    notes = models.CharField('Special details to note', max_length=300)
    keywords = models.CharField('Keywords associated with the item', max_length=300, default='')
    def __str__(self):
        return self.description + ' (' + self.destination + ')'
    def urlsafe(self):
        return urllib.parse.quote(self.description)

# TODO:
# - add image url

# wi = WasteItem(description='', destination='', notes='', keywords='')
