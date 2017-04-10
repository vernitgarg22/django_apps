from __future__ import unicode_literals

import sqlserver_ado
from sqlserver_ado.fields import BigAutoField

from django.db import models


class Sales(models.Model):
    id = sqlserver_ado.fields.BigAutoField(primary_key=True)
    pnum = models.CharField(max_length=25)
    unit = models.CharField(max_length=5)
    status = models.SmallIntegerField()
    salenum = models.SmallIntegerField()
    saledate = models.DateTimeField(blank=True, null=True)
    usecode = models.CharField(db_column='useCode', max_length=5)  # Field name made lowercase.
    saleprice = models.DecimalField(max_digits=18, decimal_places=0)
    adjsaleprice = models.DecimalField(max_digits=18, decimal_places=0)
    infadjsaleprice = models.DecimalField(max_digits=18, decimal_places=0)
    reasonsforadj = models.CharField(max_length=24)
    terms = models.CharField(max_length=20)
    instr = models.CharField(max_length=3)
    ltype = models.SmallIntegerField()
    grantor = models.CharField(max_length=35)
    grantorline2 = models.CharField(db_column='grantorLine2', max_length=35)  # Field name made lowercase.
    grantee = models.CharField(max_length=35)
    granteeline2 = models.CharField(db_column='granteeLine2', max_length=35)  # Field name made lowercase.
    propclass = models.CharField(max_length=5)
    ecftbl = models.CharField(max_length=5)
    liberpage = models.CharField(max_length=20)
    cmts = models.CharField(max_length=30)
    confidential = models.SmallIntegerField()
    verifiedby = models.CharField(max_length=14)
    dontupdate = models.SmallIntegerField()
    otherparcelsinsaleflag = models.SmallIntegerField()
    otherparcelsinsale_0 = models.CharField(max_length=25)
    otherparcelsinsale_1 = models.CharField(max_length=25)
    otherparcelsinsale_2 = models.CharField(max_length=25)
    otherparcelsinsale_3 = models.CharField(max_length=25)
    otherparcelsinsale_4 = models.CharField(max_length=25)
    pertrans = models.DecimalField(max_digits=18, decimal_places=2)
    affdate = models.DateTimeField(blank=True, null=True)
    userstr = models.CharField(max_length=15)
    usernum = models.SmallIntegerField()
    streetnumber = models.FloatField()
    streetdirect = models.CharField(max_length=2)
    streetname = models.CharField(max_length=25)
    unitorapt = models.CharField(max_length=7)
    addresscombined = models.CharField(max_length=62)
    notaff = models.SmallIntegerField(db_column='notAff')  # Field name made lowercase.
    ptafinebilled = models.SmallIntegerField(db_column='PTAFineBilled')  # Field name made lowercase.
    currentassment = models.FloatField()
    previousassment = models.FloatField()
    assmentwhensold = models.FloatField()
    curassmentsaleratio = models.FloatField()
    prevassmentsaleratio = models.FloatField()
    assmentwhensoldsaleratio = models.FloatField()
    esttcvsaleratio = models.FloatField()
    filedate = models.DateTimeField(blank=True, null=True)
    sendstatementto = models.SmallIntegerField()
    esttcv = models.FloatField()
    landvalue = models.FloatField()
    totalacres = models.FloatField()
    actualfront = models.FloatField()
    efffront = models.FloatField()
    avedepth = models.FloatField()
    improved = models.SmallIntegerField()
    landivalue = models.FloatField()
    bldgimprval = models.FloatField()
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
    agb_numagb = models.SmallIntegerField()
    agb_calcvalue = models.FloatField()
    agb_value = models.FloatField()
    nothomestead = models.SmallIntegerField(db_column='notHomestead')  # Field name made lowercase.
    pa260 = models.SmallIntegerField()
    grossrent = models.FloatField(db_column='GrossRent')  # Field name made lowercase.
    marknumber = models.IntegerField(db_column='markNumber')  # Field name made lowercase.
    netacres = models.DecimalField(db_column='netAcres', max_digits=18, decimal_places=3)  # Field name made lowercase.
    transdenial = models.SmallIntegerField(db_column='transDenial')  # Field name made lowercase.
    useinecf = models.SmallIntegerField(db_column='useInECF')  # Field name made lowercase.
    landtable = models.CharField(db_column='landTable', max_length=5)  # Field name made lowercase.
    sec108 = models.IntegerField(db_column='Sec108')  # Field name made lowercase.
    dateedited = models.DateTimeField(db_column='dateEdited', blank=True, null=True)  # Field name made lowercase.
    streetsortstring = models.CharField(db_column='streetSortString', max_length=62)  # Field name made lowercase.
    unitclasssort = models.CharField(db_column='unitClassSort', max_length=21)  # Field name made lowercase.
    unitsaledatesort = models.CharField(db_column='unitSaleDateSort', max_length=23)  # Field name made lowercase.
    pnumsort = models.CharField(db_column='pnumSort', max_length=36)  # Field name made lowercase.
    saledatesort = models.CharField(db_column='saleDateSort', max_length=10)  # Field name made lowercase.
    granteesort = models.CharField(db_column='granteeSort', max_length=46)  # Field name made lowercase.
    grantorsort = models.CharField(db_column='grantorSort', max_length=46)  # Field name made lowercase.
    liberpagesort = models.CharField(db_column='liberPageSort', max_length=31)  # Field name made lowercase.
    unitecfsort = models.CharField(db_column='unitEcfSort', max_length=22)  # Field name made lowercase.
    salepricesort = models.CharField(db_column='salePriceSort', max_length=30)  # Field name made lowercase.
    unittermssort = models.CharField(db_column='unitTermsSort', max_length=36)  # Field name made lowercase.
    unitsaletypesort = models.CharField(db_column='unitSaleTypeSort', max_length=18)  # Field name made lowercase.
    unituserasort = models.CharField(db_column='unitUserASort', max_length=32)  # Field name made lowercase.
    classsort = models.CharField(db_column='classSort', max_length=16)  # Field name made lowercase.
    unitinstsort = models.CharField(db_column='unitInstSort', max_length=19)  # Field name made lowercase.
    usecodesort = models.CharField(db_column='useCodeSort', max_length=16)  # Field name made lowercase.
    unitlandsort = models.CharField(db_column='unitLandSort', max_length=22)  # Field name made lowercase.
    isvacantlandsale = models.SmallIntegerField(db_column='isVacantLandSale')  # Field name made lowercase.
    sdredemptiondate = models.DateTimeField(db_column='sdRedemptionDate', blank=True, null=True)  # Field name made lowercase.
    sduncappingdate = models.DateTimeField(db_column='sdUncappingDate', blank=True, null=True)  # Field name made lowercase.
    flagforecf = models.SmallIntegerField(db_column='flagForEcf')  # Field name made lowercase.
    sdredemptiondatesort = models.CharField(db_column='sdRedemptionDateSort', max_length=17)  # Field name made lowercase.
    sduncappingdatesort = models.CharField(db_column='sdUncappingDateSort', max_length=17)  # Field name made lowercase.
    ptapenaltyapplies = models.SmallIntegerField(db_column='PTAPenaltyApplies')  # Field name made lowercase.
    cibbedrooms = models.SmallIntegerField(db_column='CiBBedrooms')  # Field name made lowercase.
    cibunits = models.SmallIntegerField(db_column='CiBUnits')  # Field name made lowercase.
    sentdate = models.DateTimeField(db_column='sentDate', blank=True, null=True)  # Field name made lowercase.
    padatefiled = models.DateTimeField(db_column='paDateFiled', blank=True, null=True)  # Field name made lowercase.
    additionalgrantees = models.CharField(db_column='additionalGrantees', max_length=200)  # Field name made lowercase.
    additionalgrantors = models.CharField(db_column='additionalGrantors', max_length=200)  # Field name made lowercase.
    pa260liberpage = models.CharField(db_column='pa260LiberPage', max_length=20)  # Field name made lowercase.
    importstatus = models.CharField(db_column='importStatus', max_length=30)  # Field name made lowercase.
    ptaamountbilled = models.FloatField(db_column='ptaAmountBilled')  # Field name made lowercase.
    lifeleasegrantee = models.CharField(db_column='lifeLeaseGrantee', max_length=35)  # Field name made lowercase.
    residuallandvalue = models.FloatField(db_column='residualLandValue')  # Field name made lowercase.
    daysonmarket = models.SmallIntegerField(db_column='daysOnMarket')  # Field name made lowercase.
    datesaleentered = models.DateTimeField(db_column='dateSaleEntered', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sales'

    def __str__(self):
        return str(id) + " - " + self.addresscombined

    def json(self):
        return {
            "id": self.id,
            "pnum": self.pnum,
            "saleprice": self.saleprice,
            "saledate": self.saledate,
            "addresscombined": self.addresscombined,
            "terms": self.terms,
            "instr": self.instr,
            "grantee": self.grantee,
            "grantor": self.grantor
        }


# from assessments.models import Sales
# Sales.objects.using('eql').get(id=3845977)
# Sales.objects.using("eql").filter(addresscombined__contains='7840 van dyke pl')
