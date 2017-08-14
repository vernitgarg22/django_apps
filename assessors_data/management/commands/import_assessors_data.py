import csv
from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from assessors_data.models import MttTrackerExport2017, Whd01Parcl2017


def clean_string(buffer):
    """
    Trim quotes from start and end of string
    """
    if len(buffer) >= 2 and buffer[0] == '"' and buffer[-1] == '"':
        return buffer[1:-1]
    else:
        return buffer


class Command(BaseCommand):
    help = """
        Use this to import image assessors data into warehousedb1, e.g.,
        python manage.py import_assessors_data <database> <csv_file>
        python manage.py import_assessors_data finassessorprod MTT_TRACKEREXPORT2018.csv
        python manage.py import_assessors_data warehousedb1 MTT_TRACKEREXPORT2018.csv"""

    index = 0

    def trace(self, value):
        self.stdout.write(value)
        self.stdout.flush()

    def add_arguments(self, parser):
        parser.add_argument('database', type=str, help="Database to import the database into")
        parser.add_argument('file_path', type=str, help="Path to the csv file containing the assessors data")

    def get_value(self, row, klass=str):
        value = clean_string(row[self.index])
        self.index = self.index + 1
        if not value:
            return None

        if klass == Decimal and '-' in value:
            idx = value.index('-')
            if idx > 0:
                value = value[0 : idx]

        try:
            if klass == datetime:
                dt = datetime.strptime(value, "%m/%d/%Y")
                return timezone.make_aware(dt)
            else:
                return klass(value)
        except:
            return None

    def get_data_model(self):
        return Whd01Parcl2017 if self.use_warehousedb else MttTrackerExport2017

    def parse_row(self, row):

        self.index = 0

        parcels_pnum = self.get_value(row)
        parcelmaster_ownername1 = self.get_value(row)
        parcelmaster_ownername2 = self.get_value(row)
        parcelmaster_ownercareof = self.get_value(row)
        parcelmaster_propstreetcombined = self.get_value(row)
        parcelmaster_propstreetname = self.get_value(row)
        parcelmaster_propaddrnum = self.get_value(row, Decimal)
        parcelmaster_propaddrdirect = self.get_value(row)
        parcelmaster_unitorapt = self.get_value(row)
        parcelmaster_propzip = self.get_value(row, Decimal)

        parcels_usernum = self.get_value(row, Decimal)
        parcels_mapnum = self.get_value(row, Decimal)
        parcels_exemptcode = self.get_value(row)
        parcels_ecftbl = self.get_value(row)
        parcelreadonly_adjass_0_3 = self.get_value(row, Decimal)
        parcelreadonly_ass_0 = self.get_value(row, Decimal)
        parcelreadonly_adjtax_0_3 = self.get_value(row, Decimal)
        parcelreadonly_tax_0 = self.get_value(row, Decimal)
        parcelreadonly_curclassstr = self.get_value(row)
        parcels_homestead = self.get_value(row, Decimal)

        parcels_cft_string = self.get_value(row)
        parcelmaster_relatedpnum = self.get_value(row)
        parcelmaster_lastsaledate = self.get_value(row, datetime)
        parcelmaster_lastsaleprice = self.get_value(row, Decimal)
        parcelreadonly_legaldescription = self.get_value(row)
        parcels_homedate = self.get_value(row)
        parcelmaster_mttpending_string = self.get_value(row)
        parcelmaster_taxpayname = self.get_value(row)
        parcelmaster_taxpaystreetname = self.get_value(row)
        parcelmaster_taxpaystate = self.get_value(row)

        parcelmaster_taxpayname2 = self.get_value(row)
        parcelmaster_taxpaycity = self.get_value(row)
        parcelmaster_taxpayzip = self.get_value(row)
        parcels_propclass = self.get_value(row, Decimal)
        parcels_oldprop = self.get_value(row, Decimal)
        parcels_propstatus = self.get_value(row)
        parcels_prevexemptcode = self.get_value(row)
        parcelreadonly_spactcategory = self.get_value(row)
        parcels_mborsev = self.get_value(row, Decimal)
        parcelreadonly_mborsev_1 = self.get_value(row, Decimal)

        parcelreadonly_mborsev_2 = self.get_value(row, Decimal)
        parcels_mbortax = self.get_value(row, Decimal)
        parcelreadonly_adjtax_0_2 = self.get_value(row, Decimal)
        parcelreadonly_adjtax_1_3 = self.get_value(row, Decimal)
        parcelreadonly_listnumber_0_0 = self.get_value(row)
        parcelreadonly_listnumber_1_0 = self.get_value(row)
        parcelreadonly_listnumber_2_0 = self.get_value(row)
        parcels_usecode = self.get_value(row)
        parcels_ncom = self.get_value(row, Decimal)
        parcels_newnhouse = self.get_value(row, Decimal)

        parcelmaster_resb_yearbuilt = self.get_value(row, Decimal)
        parcelmaster_resb_floorarea = self.get_value(row, Decimal)
        parcelmaster_cib_yearbuilt = self.get_value(row, Decimal)
        parcelmaster_vacant = self.get_value(row, Decimal)
        parcelmaster_resb_groundarea = self.get_value(row, Decimal)
        parcelmaster_frontage = self.get_value(row, Decimal)
        parcelmaster_landvalue = self.get_value(row, Decimal)
        parcelmaster_totalacres = self.get_value(row, Decimal)
        parcelmaster_resb_pricefloor = self.get_value(row, Decimal)
        parcelmaster_avdepth = self.get_value(row, Decimal)

        parcelmaster_landmap = self.get_value(row, Decimal)
        parcelmaster_namechgdate = self.get_value(row, datetime)
        parcelreadonly_adj_pet_dock_0_0 = self.get_value(row)
        parcelmaster_xstreetname_0 = self.get_value(row)
        parcelmaster_xstreetname_1 = self.get_value(row)
        parcelmaster_xcord = self.get_value(row, Decimal)
        parcelmaster_ycord = self.get_value(row, Decimal)
        parcelreadonly_ecftabledesc = self.get_value(row)
        parcelmaster_sub = self.get_value(row)
        parcelmaster_parcelhaslegal = self.get_value(row, Decimal)

        parcelmaster_lot = self.get_value(row)
        parcelreadonly_lastsaleliberpage = self.get_value(row)
        parcelmaster_liberpage2 = self.get_value(row)
        parcels_secunitmapnum = self.get_value(row)
        parcelmaster_mttprogress_0 = self.get_value(row)
        parcelmaster_mttyears_0 = self.get_value(row, Decimal)
        parcelmaster_lastadjustedsaleprice = self.get_value(row, Decimal)
        parcelreadonly_salefiledate = self.get_value(row, datetime)
        parcelreadonly_mostrecenttransferpercent = self.get_value(row, Decimal)

        klass = self.get_data_model()

        parcel_data = klass(parcels_pnum=parcels_pnum,
            parcelmaster_ownername1=parcelmaster_ownername1,
            parcelmaster_ownername2=parcelmaster_ownername2,
            parcelmaster_ownercareof=parcelmaster_ownercareof,
            parcelmaster_propstreetcombined=parcelmaster_propstreetcombined,
            parcelmaster_propstreetname=parcelmaster_propstreetname,
            parcelmaster_propaddrnum=parcelmaster_propaddrnum,
            parcelmaster_propaddrdirect=parcelmaster_propaddrdirect,
            parcelmaster_unitorapt=parcelmaster_unitorapt,
            parcelmaster_propzip=parcelmaster_propzip,
            parcels_usernum=parcels_usernum,
            parcels_mapnum=parcels_mapnum,
            parcels_exemptcode=parcels_exemptcode,
            parcels_ecftbl=parcels_ecftbl,
            parcelreadonly_adjass_0_3=parcelreadonly_adjass_0_3,
            parcelreadonly_ass_0=parcelreadonly_ass_0,
            parcelreadonly_adjtax_0_3=parcelreadonly_adjtax_0_3,
            parcelreadonly_tax_0=parcelreadonly_tax_0,
            parcelreadonly_curclassstr=parcelreadonly_curclassstr,
            parcels_homestead=parcels_homestead,
            parcels_cft_string=parcels_cft_string,
            parcelmaster_relatedpnum=parcelmaster_relatedpnum,
            parcelmaster_lastsaledate=parcelmaster_lastsaledate,
            parcelmaster_lastsaleprice=parcelmaster_lastsaleprice,
            parcelreadonly_legaldescription=parcelreadonly_legaldescription,
            parcels_homedate=parcels_homedate,
            parcelmaster_mttpending_string=parcelmaster_mttpending_string,
            parcelmaster_taxpayname=parcelmaster_taxpayname,
            parcelmaster_taxpaystreetname=parcelmaster_taxpaystreetname,
            parcelmaster_taxpaystate=parcelmaster_taxpaystate,
            parcelmaster_taxpayname2=parcelmaster_taxpayname2,
            parcelmaster_taxpaycity=parcelmaster_taxpaycity,
            parcelmaster_taxpayzip=parcelmaster_taxpayzip,
            parcels_propclass=parcels_propclass,
            parcels_oldprop=parcels_oldprop,
            parcels_propstatus=parcels_propstatus,
            parcels_prevexemptcode=parcels_prevexemptcode,
            parcelreadonly_spactcategory=parcelreadonly_spactcategory,
            parcels_mborsev=parcels_mborsev,
            parcelreadonly_mborsev_1=parcelreadonly_mborsev_1,
            parcelreadonly_mborsev_2=parcelreadonly_mborsev_2,
            parcels_mbortax=parcels_mbortax,
            parcelreadonly_adjtax_0_2=parcelreadonly_adjtax_0_2,
            parcelreadonly_adjtax_1_3=parcelreadonly_adjtax_1_3,
            parcelreadonly_listnumber_0_0=parcelreadonly_listnumber_0_0,
            parcelreadonly_listnumber_1_0=parcelreadonly_listnumber_1_0,
            parcelreadonly_listnumber_2_0=parcelreadonly_listnumber_2_0,
            parcels_usecode=parcels_usecode,
            parcels_ncom=parcels_ncom,
            parcels_newnhouse=parcels_newnhouse,
            parcelmaster_resb_yearbuilt=parcelmaster_resb_yearbuilt,
            parcelmaster_resb_floorarea=parcelmaster_resb_floorarea,
            parcelmaster_cib_yearbuilt=parcelmaster_cib_yearbuilt,
            parcelmaster_vacant=parcelmaster_vacant,
            parcelmaster_resb_groundarea=parcelmaster_resb_groundarea,
            parcelmaster_frontage=parcelmaster_frontage,
            parcelmaster_landvalue=parcelmaster_landvalue,
            parcelmaster_totalacres=parcelmaster_totalacres,
            parcelmaster_resb_pricefloor=parcelmaster_resb_pricefloor,
            parcelmaster_avdepth=parcelmaster_avdepth,
            parcelmaster_landmap=parcelmaster_landmap,
            parcelmaster_namechgdate=parcelmaster_namechgdate,
            parcelreadonly_adj_pet_dock_0_0=parcelreadonly_adj_pet_dock_0_0,
            parcelmaster_xstreetname_0=parcelmaster_xstreetname_0,
            parcelmaster_xstreetname_1=parcelmaster_xstreetname_1,
            parcelmaster_xcord=parcelmaster_xcord,
            parcelmaster_ycord=parcelmaster_ycord,
            parcelreadonly_ecftabledesc=parcelreadonly_ecftabledesc,
            parcelmaster_sub=parcelmaster_sub,
            parcelmaster_parcelhaslegal=parcelmaster_parcelhaslegal,
            parcelmaster_lot=parcelmaster_lot,
            parcelreadonly_lastsaleliberpage=parcelreadonly_lastsaleliberpage,
            parcelmaster_liberpage2=parcelmaster_liberpage2,
            parcels_secunitmapnum=parcels_secunitmapnum,
            parcelmaster_mttprogress_0=parcelmaster_mttprogress_0,
            parcelmaster_mttyears_0=parcelmaster_mttyears_0,
            parcelmaster_lastadjustedsaleprice=parcelmaster_lastadjustedsaleprice,
            parcelreadonly_salefiledate=parcelreadonly_salefiledate,
            parcelreadonly_mostrecenttransferpercent=parcelreadonly_mostrecenttransferpercent)

        return parcel_data

    def handle(self, *args, **options):

        if options['database'] not in [ 'finassessorprod', 'warehousedb1' ]:
            raise CommandError("Database {} is invalid".format())

        self.database = options['database']
        self.use_warehousedb = self.database == 'warehousedb1'

        file_path = options['file_path']
        first_line = True
        files={}

        with open(file_path, newline='') as csvfile:

            klass = self.get_data_model()
            klass.objects.using(self.database).all().delete()
            self.row_count = 0
            self.errors = 0

            datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
            row_data = []
            BATCHSIZE = 2500
            for row in datareader:

                if first_line:
                    first_line = False
                else:
                    row_data.append(self.parse_row(row))
                    if len(row_data) == BATCHSIZE:
                        klass.objects.using(self.database).bulk_create(row_data)
                        self.row_count = self.row_count + len(row_data)
                        self.trace("{} rows imported".format(self.row_count))
                        row_data = []

            if row_data:
                klass.objects.using(self.database).bulk_create(row_data)
                self.row_count = self.row_count + len(row_data)

            self.trace("Finished:  {} rows imported".format(self.row_count))
