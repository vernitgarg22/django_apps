from django.db import models


class Poll(models.Model):

    app_label = 'elections'

    name = models.CharField(max_length=128, unique=True, db_index=True)
    address = models.CharField(max_length=128)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    congress_rep_district = models.IntegerField()
    state_senate_district = models.IntegerField()
    state_rep_district = models.IntegerField()
    map_url = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    # REVIEW:  store the image internally (e.g, in an ImageField) or just have url like this?

    def to_json(self):
        """
        Return json representation of this object.
        """

        precincts = [ precinct.number for precinct in self.precinct_set.all() ]

        return {
            "name": self.name,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "congress_rep_district": self.congress_rep_district,
            "state_senate_district": self.state_senate_district,
            "state_rep_district": self.state_rep_district,
            "map": self.map_url,
            "image": self.image_url,
            "precincts": sorted(precincts),
        }

    def __str__(self):    # pragma: no cover - these are used mostly for debugging
        return self.name + ' - ' + self.address


class Precinct(models.Model):

    app_label = 'elections'

    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)
    number = models.IntegerField(unique=True, db_index=True)

    def __str__(self):    # pragma: no cover - these are used mostly for debugging
        return str(self.number)
