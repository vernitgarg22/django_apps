from django.db import models
from django.conf import settings


class AssessorsBase(models.Model):
    parcels_pnum = models.CharField(db_column='"Parcels pnum"', max_length=50, blank=True, null=False, primary_key=True)
    parcels_ecftbl = models.CharField(db_column='"Parcels ecftbl"', max_length=50, blank=True, null=True)
    parcelmaster_propstreetcombined = models.CharField(db_column='"ParcelMaster propstreetcombined"', max_length=50, blank=True, null=True)
    parcelmaster_propaddrnum = models.CharField(db_column='"ParcelMaster propaddrnum"', max_length=50, blank=True, null=True)
    parcelmaster_propaddrdirect = models.CharField(db_column='"ParcelMaster propaddrdirect"', max_length=50, blank=True, null=True)
    parcelmaster_propstreetname = models.CharField(db_column='"ParcelMaster propstreetname"', max_length=50, blank=True, null=True)
    parcelmaster_propzip = models.CharField(db_column='"ParcelMaster propzip"', max_length=50, blank=True, null=True)
    parcelmaster_taxpayname = models.CharField(db_column='"ParcelMaster taxpayname"', max_length=50, blank=True, null=True)
    parcelmaster_taxpayname2 = models.CharField(db_column='"ParcelMaster taxpayname2"', max_length=50, blank=True, null=True)
    parcelMaster_taxpaystreetaddr = models.CharField(db_column='"ParcelMaster taxpaystreetaddr"', max_length=50, blank=True, null=True)
    parcelmaster_taxpaycity = models.CharField(db_column='"ParcelMaster taxpaycity"', max_length=50, blank=True, null=True)
    parcelmaster_taxpaystate = models.CharField(db_column='"ParcelMaster taxpaystate"', max_length=50, blank=True, null=True)
    parcelmaster_taxpayzip = models.CharField(db_column='"ParcelMaster taxpayzip"', max_length=50, blank=True, null=True)
    parcels_propclass = models.CharField(db_column='"Parcels propclass"', max_length=50, blank=True, null=True)
    parcels_oldprop = models.CharField(db_column='"Parcels oldprop"', max_length=50, blank=True, null=True)
    parcels_propstatus = models.CharField(db_column='"Parcels propstatus"', max_length=50, blank=True, null=True)
    parcelmaster_exempt = models.CharField(db_column='"ParcelMaster exempt"', max_length=50, blank=True, null=True)
    parcels_prevexemptcode = models.CharField(db_column='"Parcels prevexemptcode"', max_length=50, blank=True, null=True)
    parcels_specialactscode = models.CharField(db_column='"Parcels specialactscode"', max_length=50, blank=True, null=True)
    memoryfieldstable_assessmentyear = models.CharField(db_column='"MemoryFieldsTable assessmentYear"', max_length=50, blank=True, null=True)
    memoryfieldstable_previousassessmentyear = models.CharField(db_column='"MemoryFieldsTable previousAssessmentYear"', max_length=50, blank=True, null=True)
    parcelreadonly_mborass1 = models.CharField(db_column='"ParcelReadonly mborass1"', max_length=50, blank=True, null=True)
    parcelreadonly_mborass2 = models.CharField(db_column='"ParcelReadonly mborass2"', max_length=50, blank=True, null=True)
    parcelreadonly_mborsev1 = models.CharField(db_column='"ParcelReadonly mborsev1"', max_length=50, blank=True, null=True)
    parcelreadonly_mborsev2 = models.CharField(db_column='"ParcelReadonly mborsev2"', max_length=50, blank=True, null=True)
    parcelreadonly_mbortax1 = models.CharField(db_column='"ParcelReadonly mbortax1"', max_length=50, blank=True, null=True)
    parcelreadonly_mbortax2 = models.CharField(db_column='"ParcelReadonly mbortax2"', max_length=50, blank=True, null=True)
    parcelmaster_specialnote = models.CharField(db_column='"ParcelMaster specialNote"', max_length=50, blank=True, null=True)
    parcels_usecode = models.CharField(db_column='"Parcels useCode"', max_length=50, blank=True, null=True)
    parcelmaster_vacant = models.CharField(db_column='"ParcelMaster vacant"', max_length=50, blank=True, null=True)
    parcelmaster_lastsaleprice = models.CharField(db_column='"ParcelMaster lastSalePrice"', max_length=50, blank=True, null=True)
    parcelmaster_lastsaledate = models.CharField(db_column='"ParcelMaster lastSaleDate"', max_length=50, blank=True, null=True)
    parcelmaster_cib_numcib = models.CharField(db_column='"ParcelMaster cib_numcib"', max_length=50, blank=True, null=True)
    parcelmaster_cib_yearbuilt = models.CharField(db_column='"ParcelMaster cib_yearbuilt"', max_length=50, blank=True, null=True)
    parcelmaster_cib_floorarea = models.CharField(db_column='"ParcelMaster cib_floorarea"', max_length=50, blank=True, null=True)
    parcelmaster_resb_numresb = models.CharField(db_column='"ParcelMaster resb_numresb"', max_length=50, blank=True, null=True)
    parcelmaster_resb_yearbuilt = models.CharField(db_column='"ParcelMaster resb_yearbuilt"', max_length=50, blank=True, null=True)
    parcelmaster_resb_groundarea = models.CharField(db_column='"ParcelMaster resb_groundarea"', max_length=50, blank=True, null=True)
    parcelmaster_totalacres = models.CharField(db_column='"ParcelMaster totalacres"', max_length=50, blank=True, null=True)
    parcels_squarefootage = models.CharField(db_column='"Parcels squareFootage"', max_length=50, blank=True, null=True)
    parcelmaster_frontage = models.CharField(db_column='"ParcelMaster frontage"', max_length=50, blank=True, null=True)
    parcelmaster_avdepth = models.CharField(db_column='"ParcelMaster avdepth"', max_length=50, blank=True, null=True)
    parcelmaster_landvalue = models.CharField(db_column='"ParcelMaster landvalue"', max_length=50, blank=True, null=True)
    parcelmaster_landmap = models.CharField(db_column='"ParcelMaster landMap"', max_length=50, blank=True, null=True)
    parcelmaster_namechgdate = models.CharField(db_column='"ParcelMaster namechgdate"', max_length=50, blank=True, null=True)
    parcelmaster_relatedpnum = models.CharField(db_column='"ParcelMaster relatedpnum"', max_length=50, blank=True, null=True)
    parcelmaster_xcord = models.CharField(db_column='"ParcelMaster XCord"', max_length=50, blank=True, null=True)
    parcelmaster_ycord = models.CharField(db_column='"ParcelMaster YCord"', max_length=50, blank=True, null=True)
    parcels_mapnum = models.CharField(db_column='"Parcels mapnum"', max_length=50, blank=True, null=True)
    neighborhoods_neighcode = models.CharField(db_column='"Neighborhoods neighcode"', max_length=50, blank=True, null=True)
    parcelmaster_block = models.CharField(db_column='"ParcelMaster block"', max_length=50, blank=True, null=True)
    parcelmaster_sub = models.CharField(db_column='"ParcelMaster sub"', max_length=50, blank=True, null=True)
    parcelmaster_liberpage = models.CharField(db_column='"ParcelMaster liberPage"', max_length=50, blank=True, null=True)
    parcelreadonly_legaldescription = models.CharField(db_column='"ParcelReadonly legalDescription"', max_length=32000, blank=True, null=True)
    parcels_usernum = models.CharField(db_column='"Parcels usernum"', max_length=50, blank=True, null=True)
    parcelmaster_ownername1 = models.CharField(db_column='"ParcelMaster ownername1"', max_length=50, blank=True, null=True)

    class Meta:
        abstract = True


    def validate(self):    # pragma: no cover (this is really just for debugging)

        for field in type(self)._meta.local_fields:
            value = self.__getattribute__(field.name)
            if type(field) == models.CharField and type(value) == str:
                if len(value) > field.max_length:
                    raise Exception("value of field {} too long".format(field.name))


class Whd01Parcl2017(AssessorsBase):
    # parcels_pnum = models.CharField(db_column='Parcels#pnum', max_length=32, blank=True, primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_ownername1 = models.CharField(db_column='ParcelMaster#ownername1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_ownername2 = models.CharField(db_column='ParcelMaster#ownername2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_ownercareof = models.CharField(db_column='ParcelMaster#ownercareof', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_propstreetcombined = models.CharField(db_column='ParcelMaster#propstreetcombined', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_propstreetname = models.CharField(db_column='ParcelMaster#propstreetname', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_propaddrnum = models.FloatField(db_column='ParcelMaster#propaddrnum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_propaddrdirect = models.CharField(db_column='ParcelMaster#propaddrdirect', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_unitorapt = models.CharField(db_column='ParcelMaster#unitorapt', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_propzip = models.FloatField(db_column='ParcelMaster#propzip', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_usernum = models.FloatField(db_column='Parcels#usernum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_mapnum = models.FloatField(db_column='Parcels#mapnum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_exemptcode = models.CharField(db_column='Parcels#exemptcode', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_ecftbl = models.CharField(db_column='Parcels#ecftbl', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_adjass_0_3 = models.FloatField(db_column='ParcelReadonly#adjass_0_3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_ass_0 = models.FloatField(db_column='ParcelReadonly#ass_0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_adjtax_0_3 = models.FloatField(db_column='ParcelReadonly#adjtax_0_3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_tax_0 = models.FloatField(db_column='ParcelReadonly#tax_0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_curclassstr = models.CharField(db_column='ParcelReadonly#curClassStr', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_homestead = models.FloatField(db_column='Parcels#homestead', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_cft_string = models.CharField(db_column='Parcels#cft_String', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_relatedpnum = models.CharField(db_column='ParcelMaster#relatedpnum', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_lastsaledate = models.DateTimeField(db_column='ParcelMaster#lastSaleDate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_lastsaleprice = models.FloatField(db_column='ParcelMaster#lastSalePrice', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_legaldescription = models.TextField(db_column='ParcelReadonly#legalDescription', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_homedate = models.CharField(db_column='Parcels#homedate', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_mttpending_string = models.CharField(db_column='ParcelMaster#MTTPending_String', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_taxpayname = models.CharField(db_column='ParcelMaster#taxpayname', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_taxpaystreetname = models.CharField(db_column='ParcelMaster#taxpayStreetName', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_taxpaystate = models.CharField(db_column='ParcelMaster#taxpaystate', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_taxpayname2 = models.CharField(db_column='ParcelMaster#taxpayname2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_taxpaycity = models.CharField(db_column='ParcelMaster#taxpaycity', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_taxpayzip = models.CharField(db_column='ParcelMaster#taxpayzip', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_propclass = models.FloatField(db_column='Parcels#propclass', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_oldprop = models.FloatField(db_column='Parcels#oldprop', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_propstatus = models.CharField(db_column='Parcels#propstatus', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_prevexemptcode = models.CharField(db_column='Parcels#prevexemptcode', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_spactcategory = models.CharField(db_column='ParcelReadonly#spActCategory', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_mborsev = models.FloatField(db_column='Parcels#mborsev', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_mborsev_1 = models.FloatField(db_column='ParcelReadonly#mborsev_1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_mborsev_2 = models.FloatField(db_column='ParcelReadonly#mborsev_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_mbortax = models.FloatField(db_column='Parcels#mbortax', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_adjtax_0_2 = models.FloatField(db_column='ParcelReadonly#adjtax_0_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_adjtax_1_3 = models.FloatField(db_column='ParcelReadonly#adjtax_1_3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_listnumber_0_0 = models.CharField(db_column='ParcelReadonly#listNumber_0_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_listnumber_1_0 = models.CharField(db_column='ParcelReadonly#listNumber_1_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_listnumber_2_0 = models.CharField(db_column='ParcelReadonly#listNumber_2_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_usecode = models.CharField(db_column='Parcels#useCode', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_ncom = models.FloatField(db_column='Parcels#ncom', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_newnhouse = models.FloatField(db_column='Parcels#newnhouse', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_resb_yearbuilt = models.FloatField(db_column='ParcelMaster#resb_yearbuilt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_resb_floorarea = models.FloatField(db_column='ParcelMaster#resb_floorarea', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_cib_yearbuilt = models.FloatField(db_column='ParcelMaster#cib_yearbuilt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_vacant = models.FloatField(db_column='ParcelMaster#vacant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_resb_groundarea = models.FloatField(db_column='ParcelMaster#resb_groundarea', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_frontage = models.FloatField(db_column='ParcelMaster#frontage', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_landvalue = models.FloatField(db_column='ParcelMaster#landvalue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_totalacres = models.FloatField(db_column='ParcelMaster#totalacres', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_resb_pricefloor = models.FloatField(db_column='ParcelMaster#resb_pricefloor', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_avdepth = models.FloatField(db_column='ParcelMaster#avdepth', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_landmap = models.FloatField(db_column='ParcelMaster#landMap', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_namechgdate = models.DateTimeField(db_column='ParcelMaster#namechgdate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_adj_pet_dock_0_0 = models.CharField(db_column='ParcelReadonly#adj_pet_dock_0_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_xstreetname_0 = models.CharField(db_column='ParcelMaster#xStreetName_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_xstreetname_1 = models.CharField(db_column='ParcelMaster#xStreetName_1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_xcord = models.FloatField(db_column='ParcelMaster#XCord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_ycord = models.FloatField(db_column='ParcelMaster#YCord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_ecftabledesc = models.CharField(db_column='ParcelReadonly#ecftableDesc', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_sub = models.CharField(db_column='ParcelMaster#sub', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_parcelhaslegal = models.FloatField(db_column='ParcelMaster#parcelHasLegal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_lot = models.CharField(db_column='ParcelMaster#lot', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_lastsaleliberpage = models.CharField(db_column='ParcelReadonly#lastSaleLiberPage', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_liberpage2 = models.CharField(db_column='ParcelMaster#liberPage2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcels_secunitmapnum = models.CharField(db_column='Parcels#secUnitMapNum', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_mttprogress_0 = models.CharField(db_column='ParcelMaster#MTTProgress_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_mttyears_0 = models.FloatField(db_column='ParcelMaster#MTTYears_0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelmaster_lastadjustedsaleprice = models.FloatField(db_column='ParcelMaster#lastAdjustedSalePrice', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_salefiledate = models.CharField(db_column='ParcelReadonly#salefiledate', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # parcelreadonly_mostrecenttransferpercent = models.FloatField(db_column='ParcelReadonly#mostRecentTransferPercent', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'WHD01_PARCL_2017'


class MttTrackerExportTest(models.Model):
    parcels_pnum = models.CharField(db_column='Parcels.pnum', max_length=25, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_ecftbl = models.CharField(db_column='Parcels.ecftbl', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propstreetcombined = models.CharField(db_column='ParcelMaster.propstreetcombined', max_length=62, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propaddrnum = models.FloatField(db_column='ParcelMaster.propaddrnum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propaddrdirect = models.CharField(db_column='ParcelMaster.propaddrdirect', max_length=1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propstreetname = models.CharField(db_column='ParcelMaster.propstreetname', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propzip = models.CharField(db_column='ParcelMaster.propzip', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpayname = models.CharField(db_column='ParcelMaster.taxpayname', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpayname2 = models.CharField(db_column='ParcelMaster.taxpayname2', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpaystreetaddr = models.CharField(db_column='ParcelMaster.taxpaystreetaddr', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpaycity = models.CharField(db_column='ParcelMaster.taxpaycity', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpaystate = models.CharField(db_column='ParcelMaster.taxpaystate', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpayzip = models.CharField(db_column='ParcelMaster.taxpayzip', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_propclass = models.CharField(db_column='Parcels.propclass', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_oldprop = models.CharField(db_column='Parcels.oldprop', max_length=8, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_propstatus = models.CharField(db_column='Parcels.propstatus', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_exempt = models.IntegerField(db_column='ParcelMaster.exempt')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_prevexemptcode = models.CharField(db_column='Parcels.prevexemptcode', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_specialactscode = models.CharField(db_column='Parcels.SpecialActsCode', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    memoryfieldstable_assessmentyear = models.IntegerField(db_column='MemoryFieldsTable.assessmentYear', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    memoryfieldstable_previousassessmentyear = models.IntegerField(db_column='MemoryFieldsTable.previousAssessmentYear', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mborass_1 = models.FloatField(db_column='ParcelReadonly.mborass_1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mborass_2 = models.FloatField(db_column='ParcelReadonly.mborass_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mborsev_1 = models.FloatField(db_column='ParcelReadonly.mborsev_1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mborsev_2 = models.FloatField(db_column='ParcelReadonly.mborsev_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mbortax_1 = models.FloatField(db_column='ParcelReadonly.mbortax_1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mbortax_2 = models.FloatField(db_column='ParcelReadonly.mbortax_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_specialnote = models.CharField(db_column='ParcelMaster.specialNote', max_length=128, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_usecode = models.CharField(db_column='Parcels.useCode', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_vacant = models.IntegerField(db_column='ParcelMaster.vacant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_lastsaleprice = models.IntegerField(db_column='ParcelMaster.lastSalePrice', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_lastsaledate = models.CharField(db_column='ParcelMaster.lastSaleDate', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_cib_numcib = models.IntegerField(db_column='ParcelMaster.cib_numcib', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_cib_yearbuilt = models.IntegerField(db_column='ParcelMaster.cib_yearbuilt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_cib_floorarea = models.IntegerField(db_column='ParcelMaster.cib_floorarea', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_numresb = models.IntegerField(db_column='ParcelMaster.resb_numresb', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_yearbuilt = models.IntegerField(db_column='ParcelMaster.resb_yearbuilt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_groundarea = models.IntegerField(db_column='ParcelMaster.resb_groundarea', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_totalacres = models.FloatField(db_column='ParcelMaster.totalacres', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_squarefootage = models.IntegerField(db_column='Parcels.squareFootage', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_frontage = models.IntegerField(db_column='ParcelMaster.frontage', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_avdepth = models.IntegerField(db_column='ParcelMaster.avdepth', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_landvalue = models.IntegerField(db_column='ParcelMaster.landvalue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_landmap = models.CharField(db_column='ParcelMaster.landMap', max_length=8, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_namechgdate = models.CharField(db_column='ParcelMaster.namechgdate', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_relatedpnum = models.CharField(db_column='ParcelMaster.relatedpnum', max_length=48, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_xcord = models.FloatField(db_column='ParcelMaster.XCord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_ycord = models.FloatField(db_column='ParcelMaster.YCord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_mapnum = models.CharField(db_column='Parcels.mapnum', max_length=8, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    neighborhoods_neighcode = models.CharField(db_column='Neighborhoods.neighcode', max_length=8, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_block = models.CharField(db_column='ParcelMaster.block', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_sub = models.CharField(db_column='ParcelMaster.sub', max_length=32, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_liberpage = models.CharField(db_column='ParcelMaster.liberpage', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_legaldescription = models.CharField(db_column='ParcelReadonly.legalDescription', max_length=32000, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_usernum = models.IntegerField(db_column='Parcels.usernum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_ownername1 = models.CharField(db_column='ParcelMaster.ownername1', max_length=48, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    def validate(self):    # pragma: no cover (this is really just for debugging)

        for field in type(self)._meta.local_fields:
            value = self.__getattribute__(field.name)
            if type(field) == models.CharField and type(value) == str:
                if len(value) > field.max_length:

                    raise Exception("value of field {} too long".format(field.name))

    class Meta:
        managed = False
        db_table = 'MTT_TRACKEREXPORT_TEST'

