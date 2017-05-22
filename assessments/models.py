from __future__ import unicode_literals

import sqlserver_ado
from sqlserver_ado.fields import BigAutoField

from django.db import models
from django.conf import settings

from assessments import util


class Sales(models.Model):

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        id = sqlserver_ado.fields.BigAutoField(primary_key=True)
   
    pnum = models.CharField(max_length=25)
    saledate = models.DateTimeField(blank=True, null=True)
    addresscombined = models.CharField(max_length=62)
    saleprice = models.DecimalField(max_digits=18, decimal_places=0)
    terms = models.CharField(max_length=20)
    instr = models.CharField(max_length=3)
    grantor = models.CharField(max_length=35)
    grantee = models.CharField(max_length=35)

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'Sales'

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

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        id = sqlserver_ado.fields.BigAutoField(primary_key=True)

    pnum = models.CharField(unique=True, max_length=25)
    relatedpnum = models.CharField(max_length=25)
    propstreetcombined = models.CharField(max_length=62)
    ownername1 = models.CharField(max_length=35)
    ownername2 = models.CharField(max_length=35)
    ownerstreetaddr = models.CharField(max_length=35)
    ownercity = models.CharField(max_length=25)
    ownerstate = models.CharField(max_length=2)
    ownerzip = models.CharField(max_length=10)
    xstreetname_0 = models.CharField(db_column='xStreetName_0', max_length=25)
    xstreetname_1 = models.CharField(db_column='xStreetName_1', max_length=25)

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
    resb_gartype = models.SmallIntegerField(db_column='resb_garType')
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
    cibbedrooms = models.SmallIntegerField(db_column='CiBBedrooms')
    cibunits = models.SmallIntegerField(db_column='CiBUnits')

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'ParcelMaster'

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


#
# from oracle tidemark database ...
#

class RoleType(models.Model):
    role_type = models.CharField(primary_key=True, max_length=3)
    role_description = models.CharField(max_length=50, blank=True, null=True)
    role_related_to = models.CharField(max_length=1, blank=True, null=True)
    role_updated = models.DateField(blank=True, null=True)
    role_updateby = models.CharField(max_length=4, blank=True, null=True)

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'role_type'


class Parcel(models.Model):
    prc_parcel_no = models.CharField(primary_key=True, max_length=30)
    prc_avp_no = models.BigIntegerField()
    prc_vp_no = models.BigIntegerField()
    prc_updated = models.DateField(blank=True, null=True)
    prc_updated_by = models.CharField(max_length=4, blank=True, null=True)
    prc_notes = models.TextField(blank=True, null=True)  # This field type is a guess.
    prc_status = models.CharField(max_length=1, blank=True, null=True)
    prc_subdiv = models.CharField(max_length=50, blank=True, null=True)
    prc_lot = models.CharField(max_length=10, blank=True, null=True)
    prc_block = models.CharField(max_length=5, blank=True, null=True)
    prc_quarter = models.CharField(max_length=2, blank=True, null=True)
    prc_section = models.CharField(max_length=2, blank=True, null=True)
    prc_township = models.CharField(max_length=2, blank=True, null=True)
    prc_range = models.CharField(max_length=2, blank=True, null=True)
    prc_zoning = models.CharField(max_length=5, blank=True, null=True)
    prc_census_tract = models.CharField(max_length=6, blank=True, null=True)
    prc_census_blk = models.CharField(max_length=6, blank=True, null=True)
    prc_size = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    prc_land_use = models.CharField(max_length=10, blank=True, null=True)
    prc_expt_code = models.CharField(max_length=3, blank=True, null=True)
    prc_fcv_land = models.BigIntegerField(blank=True, null=True)
    prc_fcv_improv = models.IntegerField(blank=True, null=True)
    prc_sale_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    prc_trnsfr_date = models.DateField(blank=True, null=True)
    prc_legal_desc = models.CharField(max_length=255, blank=True, null=True)
    prc_zip_code = models.CharField(max_length=10, blank=True, null=True)
    prc_township_sfx = models.CharField(max_length=1, blank=True, null=True)
    prc_range_sfx = models.CharField(max_length=1, blank=True, null=True)
    prc_acres = models.CharField(max_length=2, blank=True, null=True)
    prc_legal_lot = models.CharField(max_length=1, blank=True, null=True)
    prc_insp_district = models.CharField(max_length=4, blank=True, null=True)
    prc_cluster_sector = models.CharField(max_length=4, blank=True, null=True)
    prc_prop_class = models.CharField(max_length=5, blank=True, null=True)
    prc_prev_class = models.CharField(max_length=5, blank=True, null=True)
    prc_tax_status = models.CharField(max_length=30, blank=True, null=True)
    prc_prev_tax_status = models.CharField(max_length=30, blank=True, null=True)
    prc_ci_bldg_no = models.BigIntegerField(blank=True, null=True)
    prc_ci_yr_built = models.BigIntegerField(blank=True, null=True)
    prc_ci_flr_area = models.BigIntegerField(blank=True, null=True)
    prc_r_bldg_no = models.BigIntegerField(blank=True, null=True)
    prc_r_yr_built = models.BigIntegerField(blank=True, null=True)
    prc_r_gnd_area = models.BigIntegerField(blank=True, null=True)
    prc_land_map = models.BigIntegerField(blank=True, null=True)
    prc_xstreet1 = models.CharField(max_length=30, blank=True, null=True)
    prc_xstreet2 = models.CharField(max_length=30, blank=True, null=True)
    prc_mapid = models.BigIntegerField(blank=True, null=True)
    prc_aka_addr = models.CharField(max_length=50, blank=True, null=True)
    prc_nghb_code = models.CharField(max_length=10, blank=True, null=True)
    prc_nsp_code = models.CharField(max_length=30, blank=True, null=True)

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'parcel'
            unique_together = (('prc_parcel_no', 'prc_avp_no'),)


    IGNORED_FIELDS = [ 'casemain' ]

    def json(self):     # pragma: no cover - these are used mostly for debugging

        json = {}
        fields = self._meta.get_fields()
        for field in fields:
            value = getattr(self, field.name)
            json[field.name] = util.clean_parcel_val(value)

        return json

    def pp(self):     # pragma: no cover - these are used mostly for debugging

        fields = self._meta.get_fields()
        for field in fields:
            if field.name not in Parcel.IGNORED_FIELDS:
                value = getattr(self, field.name)
                print(field.name + ': ' + str(util.clean_parcel_val(value)))


class CaseType(models.Model):
    case_type = models.CharField(primary_key=True, max_length=3)
    role_type = models.ForeignKey('RoleType', db_column='role_type')
    cst_description = models.CharField(max_length=50, blank=True, null=True)
    cst_prcl_flag = models.CharField(max_length=1, blank=True, null=True)
    cst_type = models.CharField(max_length=1, blank=True, null=True)
    cst_sequence = models.IntegerField(blank=True, null=True)
    cst_updateby = models.CharField(max_length=4, blank=True, null=True)
    cst_use_yr = models.CharField(max_length=1, blank=True, null=True)
    cst_year = models.CharField(max_length=4, blank=True, null=True)
    cst_updated = models.DateField(blank=True, null=True)
    cst_fee_date_fld = models.CharField(max_length=3, blank=True, null=True)
    cst_case_dw = models.CharField(max_length=30, blank=True, null=True)
    cst_header_dw = models.CharField(max_length=30, blank=True, null=True)
    cst_exp_date_func = models.CharField(max_length=35, blank=True, null=True)
    cst_exp_date_param = models.CharField(max_length=80, blank=True, null=True)
    cst_summary_rpt = models.CharField(max_length=50, blank=True, null=True)

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'case_type'


class CaseMain(models.Model):
    csm_caseno = models.CharField(primary_key=True, max_length=14)
    case_type = models.ForeignKey(CaseType, db_column='case_type', related_name='type')
    prc_parcel_no = models.ForeignKey('Parcel', db_column='prc_parcel_no', related_name='parcel_no')
    csm_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    csm_target_date = models.DateField(blank=True, null=True)
    prc_avp_no = models.ForeignKey('Parcel', db_column='prc_avp_no', related_name='avp_no')
    csm_expr_date = models.DateField(blank=True, null=True)
    csm_finaled_date = models.DateField(blank=True, null=True)
    csm_issued_date = models.DateField(blank=True, null=True)
    csm_name_first = models.CharField(max_length=35, blank=True, null=True)
    csm_name_last = models.CharField(max_length=35, blank=True, null=True)
    csm_name_mi = models.CharField(max_length=1, blank=True, null=True)
    csm_projname = models.CharField(max_length=30, blank=True, null=True)
    csm_recd_by = models.CharField(max_length=16, blank=True, null=True)
    csm_recd_date = models.DateField(blank=True, null=True)
    csm_status = models.CharField(max_length=3, blank=True, null=True)
    csm_frozen = models.CharField(max_length=1, blank=True, null=True)
    csm_auto_cond = models.CharField(max_length=3, blank=True, null=True)
    csm_updateby = models.CharField(max_length=4, blank=True, null=True)
    csm_updated = models.DateField(blank=True, null=True)
    csm_projno = models.CharField(max_length=14, blank=True, null=True)
    csm_mastno = models.CharField(max_length=14, blank=True, null=True)
    csm_tracking_no = models.BigIntegerField(blank=True, null=True)

    if not settings.RUNNING_UNITTESTS: # pragma: no cover
        class Meta:
            managed = False
            db_table = 'casemain'

    def json(self):
        return {
            "csm_caseno": self.csm_caseno,
            "case_type": self.case_type.case_type,
            "prc_parcel_no": self.prc_parcel_no.prc_parcel_no,
            "csm_description": self.csm_description,
            "csm_target_date": self.csm_target_date,
            "prc_avp_no": self.prc_avp_no.prc_parcel_no,
        }
