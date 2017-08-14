from django.db import models
from django.conf import settings


class Whd01Parcl2017(models.Model):
    # parcels_pnum = models.FloatField(db_column='Parcels#pnum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_pnum = models.CharField(db_column='Parcels#pnum', max_length=32, blank=True, primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_ownername1 = models.CharField(db_column='ParcelMaster#ownername1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_ownername2 = models.CharField(db_column='ParcelMaster#ownername2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_ownercareof = models.CharField(db_column='ParcelMaster#ownercareof', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propstreetcombined = models.CharField(db_column='ParcelMaster#propstreetcombined', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propstreetname = models.CharField(db_column='ParcelMaster#propstreetname', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propaddrnum = models.FloatField(db_column='ParcelMaster#propaddrnum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propaddrdirect = models.CharField(db_column='ParcelMaster#propaddrdirect', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_unitorapt = models.CharField(db_column='ParcelMaster#unitorapt', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_propzip = models.FloatField(db_column='ParcelMaster#propzip', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_usernum = models.FloatField(db_column='Parcels#usernum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_mapnum = models.FloatField(db_column='Parcels#mapnum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_exemptcode = models.CharField(db_column='Parcels#exemptcode', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_ecftbl = models.CharField(db_column='Parcels#ecftbl', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_adjass_0_3 = models.FloatField(db_column='ParcelReadonly#adjass_0_3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_ass_0 = models.FloatField(db_column='ParcelReadonly#ass_0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_adjtax_0_3 = models.FloatField(db_column='ParcelReadonly#adjtax_0_3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_tax_0 = models.FloatField(db_column='ParcelReadonly#tax_0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_curclassstr = models.CharField(db_column='ParcelReadonly#curClassStr', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_homestead = models.FloatField(db_column='Parcels#homestead', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_cft_string = models.CharField(db_column='Parcels#cft_String', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_relatedpnum = models.CharField(db_column='ParcelMaster#relatedpnum', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_lastsaledate = models.DateTimeField(db_column='ParcelMaster#lastSaleDate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_lastsaleprice = models.FloatField(db_column='ParcelMaster#lastSalePrice', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_legaldescription = models.TextField(db_column='ParcelReadonly#legalDescription', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_homedate = models.CharField(db_column='Parcels#homedate', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_mttpending_string = models.CharField(db_column='ParcelMaster#MTTPending_String', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpayname = models.CharField(db_column='ParcelMaster#taxpayname', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpaystreetname = models.CharField(db_column='ParcelMaster#taxpayStreetName', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpaystate = models.CharField(db_column='ParcelMaster#taxpaystate', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpayname2 = models.CharField(db_column='ParcelMaster#taxpayname2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpaycity = models.CharField(db_column='ParcelMaster#taxpaycity', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_taxpayzip = models.CharField(db_column='ParcelMaster#taxpayzip', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_propclass = models.FloatField(db_column='Parcels#propclass', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_oldprop = models.FloatField(db_column='Parcels#oldprop', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_propstatus = models.CharField(db_column='Parcels#propstatus', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_prevexemptcode = models.CharField(db_column='Parcels#prevexemptcode', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_spactcategory = models.CharField(db_column='ParcelReadonly#spActCategory', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_mborsev = models.FloatField(db_column='Parcels#mborsev', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mborsev_1 = models.FloatField(db_column='ParcelReadonly#mborsev_1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mborsev_2 = models.FloatField(db_column='ParcelReadonly#mborsev_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_mbortax = models.FloatField(db_column='Parcels#mbortax', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_adjtax_0_2 = models.FloatField(db_column='ParcelReadonly#adjtax_0_2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_adjtax_1_3 = models.FloatField(db_column='ParcelReadonly#adjtax_1_3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_listnumber_0_0 = models.CharField(db_column='ParcelReadonly#listNumber_0_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_listnumber_1_0 = models.CharField(db_column='ParcelReadonly#listNumber_1_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_listnumber_2_0 = models.CharField(db_column='ParcelReadonly#listNumber_2_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_usecode = models.CharField(db_column='Parcels#useCode', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_ncom = models.FloatField(db_column='Parcels#ncom', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_newnhouse = models.FloatField(db_column='Parcels#newnhouse', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_yearbuilt = models.FloatField(db_column='ParcelMaster#resb_yearbuilt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_floorarea = models.FloatField(db_column='ParcelMaster#resb_floorarea', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_cib_yearbuilt = models.FloatField(db_column='ParcelMaster#cib_yearbuilt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_vacant = models.FloatField(db_column='ParcelMaster#vacant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_groundarea = models.FloatField(db_column='ParcelMaster#resb_groundarea', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_frontage = models.FloatField(db_column='ParcelMaster#frontage', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_landvalue = models.FloatField(db_column='ParcelMaster#landvalue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_totalacres = models.FloatField(db_column='ParcelMaster#totalacres', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_resb_pricefloor = models.FloatField(db_column='ParcelMaster#resb_pricefloor', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_avdepth = models.FloatField(db_column='ParcelMaster#avdepth', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_landmap = models.FloatField(db_column='ParcelMaster#landMap', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_namechgdate = models.DateTimeField(db_column='ParcelMaster#namechgdate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_adj_pet_dock_0_0 = models.CharField(db_column='ParcelReadonly#adj_pet_dock_0_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_xstreetname_0 = models.CharField(db_column='ParcelMaster#xStreetName_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_xstreetname_1 = models.CharField(db_column='ParcelMaster#xStreetName_1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_xcord = models.FloatField(db_column='ParcelMaster#XCord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_ycord = models.FloatField(db_column='ParcelMaster#YCord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_ecftabledesc = models.CharField(db_column='ParcelReadonly#ecftableDesc', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_sub = models.CharField(db_column='ParcelMaster#sub', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_parcelhaslegal = models.FloatField(db_column='ParcelMaster#parcelHasLegal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_lot = models.CharField(db_column='ParcelMaster#lot', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_lastsaleliberpage = models.CharField(db_column='ParcelReadonly#lastSaleLiberPage', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_liberpage2 = models.CharField(db_column='ParcelMaster#liberPage2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcels_secunitmapnum = models.CharField(db_column='Parcels#secUnitMapNum', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_mttprogress_0 = models.CharField(db_column='ParcelMaster#MTTProgress_0', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_mttyears_0 = models.FloatField(db_column='ParcelMaster#MTTYears_0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelmaster_lastadjustedsaleprice = models.FloatField(db_column='ParcelMaster#lastAdjustedSalePrice', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_salefiledate = models.CharField(db_column='ParcelReadonly#salefiledate', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parcelreadonly_mostrecenttransferpercent = models.FloatField(db_column='ParcelReadonly#mostRecentTransferPercent', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'WHD01_PARCL_2017'
