from __future__ import unicode_literals

import sqlserver_ado
from sqlserver_ado.fields import BigAutoField

from django.db import models

from assessments import util


class Sales(models.Model):
    # id = sqlserver_ado.fields.BigAutoField(primary_key=True)
    pnum = models.CharField(max_length=25)
    saledate = models.DateTimeField(blank=True, null=True)
    addresscombined = models.CharField(max_length=62)
    saleprice = models.DecimalField(max_digits=18, decimal_places=0)
    terms = models.CharField(max_length=20)
    instr = models.CharField(max_length=3)
    grantor = models.CharField(max_length=35)
    grantee = models.CharField(max_length=35)

    # class Meta:
    #     managed = False
    #     db_table = 'Sales'

    def __str__(self):
        return str(id) + ' - ' + self.pnum + " - " + self.addresscombined

    def json(self):
        return {
            "pnum": self.pnum,
            "saleprice": self.saleprice,
            "saledate": self.saledate,
            "addresscombined": self.addresscombined,
            "terms": self.terms,
            "instr": self.instr,
            "grantee": self.grantee,
            "grantor": self.grantor
        }


class ParcelMaster(models.Model):

    IGNORED_FIELDS = [ 'id' ]

    # id = sqlserver_ado.fields.BigAutoField(primary_key=True)
    pnum = models.CharField(unique=True, max_length=25)
    relatedpnum = models.CharField(max_length=25)
    propstreetcombined = models.CharField(max_length=62)
    ownername1 = models.CharField(max_length=35)
    ownername2 = models.CharField(max_length=35)
    ownerstreetaddr = models.CharField(max_length=35)
    ownercity = models.CharField(max_length=25)
    ownerstate = models.CharField(max_length=2)
    ownerzip = models.CharField(max_length=10)
    xstreetname_0 = models.CharField(db_column='xStreetName_0', max_length=25)  # Field name made lowercase.
    xstreetname_1 = models.CharField(db_column='xStreetName_1', max_length=25)  # Field name made lowercase.

    resb_numresb = models.SmallIntegerField()
    resb_occ = models.SmallIntegerField()
    resb_styhgt = models.SmallIntegerField()
    resb_yearbuilt = models.SmallIntegerField()
    resb_bldgclass = models.SmallIntegerField()
    resb_plusminus = models.SmallIntegerField()
    resb_style = models.CharField(max_length=15)
    resb_effage = models.SmallIntegerField()
    resb_depr = models.SmallIntegerField()
    resb_heat = models.SmallIntegerField()
    resb_nbed = models.SmallIntegerField()
    resb_fullbaths = models.SmallIntegerField()
    resb_halfbaths = models.SmallIntegerField()
    resb_gartype = models.SmallIntegerField(db_column='resb_garType')  # Field name made lowercase.
    resb_fireplaces = models.SmallIntegerField()
    resb_exterior = models.SmallIntegerField()
    resb_floorarea = models.IntegerField()
    resb_groundarea = models.IntegerField()
    resb_basementarea = models.IntegerField()
    resb_garagearea = models.IntegerField()
    resb_avestyht = models.FloatField()
    resb_pricefloor = models.FloatField()
    resb_priceground = models.FloatField()
    resb_calcvalue = models.FloatField()
    resb_value = models.FloatField()

    cib_numcib = models.SmallIntegerField()
    cib_occ = models.SmallIntegerField()
    cib_yearbuilt = models.SmallIntegerField()
    cib_bldgclass = models.SmallIntegerField()
    cib_effage = models.SmallIntegerField()
    cib_stories = models.SmallIntegerField()
    cib_floorarea = models.FloatField()
    cib_pricefloor = models.FloatField()
    cib_calcvalue = models.FloatField()
    cib_value = models.FloatField()
    cibbedrooms = models.SmallIntegerField(db_column='CiBBedrooms')  # Field name made lowercase.
    cibunits = models.SmallIntegerField(db_column='CiBUnits')  # Field name made lowercase.

    # class Meta:
    #     managed = False
    #     db_table = 'ParcelMaster'

    def __str__(self):
        return str(id) + ' - ' + self.pnum + " - " + self.propstreetcombined

    def json(self):

        json = {}
        fields = self._meta.get_fields()
        for field in fields:
            if field.name not in ParcelMaster.IGNORED_FIELDS:
                value = getattr(self, field.name)
                json[field.name] = util.clean_parcel_val(value)

        return json
