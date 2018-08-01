from django.db import models


class District(models.Model):

    app_label = 'elections'

    number = models.IntegerField(unique=True, db_index=True)

    def __str__(self):    # pragma: no cover - these are used mostly for debugging
        return str(self.number)


# REVIEW TODO oops districts should be congressional versus state


class Poll(models.Model):

    app_label = 'elections'

    name = models.CharField(max_length=128, unique=True, db_index=True)
    address = models.CharField(max_length=128)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
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
            "district": self.district.number,
            "map": self.map_url,
            "image": self.image_url,
            "precincts": precincts,
        }

    def __str__(self):    # pragma: no cover - these are used mostly for debugging
        return self.name + ' - ' + self.address


class Precinct(models.Model):

    app_label = 'elections'

    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    number = models.IntegerField(unique=True, db_index=True)

    def __str__(self):    # pragma: no cover - these are used mostly for debugging
        return str(self.number)
