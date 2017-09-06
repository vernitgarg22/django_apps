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
        parcels_ecftbl = self.get_value(row)
        parcelmaster_propstreetcombined = self.get_value(row)
        parcelmaster_propaddrnum = self.get_value(row, Decimal)
        parcelmaster_propaddrdirect = self.get_value(row)
        parcelmaster_propstreetname = self.get_value(row)
        parcelmaster_propzip = self.get_value(row, Decimal)
        parcelmaster_taxpayname = self.get_value(row)
        parcelmaster_taxpayname2 = self.get_value(row)
        parcelMaster_taxpaystreetaddr = self.get_value(row)

        parcelmaster_taxpaycity = self.get_value(row)
        parcelmaster_taxpaystate = self.get_value(row)
        parcelmaster_taxpayzip = self.get_value(row)
        parcels_propclass = self.get_value(row, Decimal)
        parcels_oldprop = self.get_value(row, Decimal)
        parcels_propstatus = self.get_value(row)
        parcelmaster_exempt = self.get_value(row)
        parcels_prevexemptcode = self.get_value(row)
        parcels_specialactscode = self.get_value(row)
        memoryfieldstable_assessmentyear = self.get_value(row, Decimal)

        memoryfieldstable_previousassessmentyear = self.get_value(row, Decimal)
        parcelreadonly_mborass1 = self.get_value(row, Decimal)
        parcelreadonly_mborass2 = self.get_value(row, Decimal)
        parcelreadonly_mborsev1 = self.get_value(row, Decimal)
        parcelreadonly_mborsev2 = self.get_value(row, Decimal)
        parcelreadonly_mbortax1 = self.get_value(row, Decimal)
        parcelreadonly_mbortax2 = self.get_value(row, Decimal)
        parcelmaster_specialnote = self.get_value(row)
        parcels_usecode = self.get_value(row)
        parcelmaster_vacant = self.get_value(row, Decimal)

        parcelmaster_lastsaleprice = self.get_value(row, Decimal)
        parcelmaster_lastsaledate = self.get_value(row, datetime)
        parcelmaster_cib_numcib = self.get_value(row, Decimal)
        parcelmaster_cib_yearbuilt = self.get_value(row, Decimal)
        parcelmaster_cib_floorarea = self.get_value(row, Decimal)
        parcelmaster_resb_numresb = self.get_value(row, Decimal)
        parcelmaster_resb_yearbuilt = self.get_value(row, Decimal)
        parcelmaster_resb_groundarea = self.get_value(row, Decimal)
        parcelmaster_totalacres = self.get_value(row, Decimal)
        parcels_squarefootage = self.get_value(row, Decimal)

        parcelmaster_frontage = self.get_value(row, Decimal)
        parcelmaster_avdepth = self.get_value(row, Decimal)
        parcelmaster_landvalue = self.get_value(row, Decimal)
        parcelmaster_landmap = self.get_value(row, Decimal)
        parcelmaster_namechgdate = self.get_value(row, datetime)
        parcelmaster_relatedpnum = self.get_value(row)
        parcelmaster_xcord = self.get_value(row, Decimal)
        parcelmaster_ycord = self.get_value(row, Decimal)
        parcels_mapnum = self.get_value(row, Decimal)
        neighborhoods_neighcode = self.get_value(row, Decimal)

        parcelmaster_block = self.get_value(row, Decimal)
        parcelmaster_sub = self.get_value(row, Decimal)
        parcelmaster_liberpage = self.get_value(row, Decimal)
        parcelreadonly_legaldescription = self.get_value(row)
        parcels_usernum = self.get_value(row, Decimal)
        parcelmaster_ownername1 = self.get_value(row)

        klass = self.get_data_model()

        parcel_data = klass(parcels_pnum=parcels_pnum,
            parcels_ecftbl=parcels_ecftbl,
            parcelmaster_propstreetcombined=parcelmaster_propstreetcombined,
            parcelmaster_propaddrnum=parcelmaster_propaddrnum,
            parcelmaster_propaddrdirect=parcelmaster_propaddrdirect,
            parcelmaster_propstreetname=parcelmaster_propstreetname,
            parcelmaster_propzip=parcelmaster_propzip,
            parcelmaster_taxpayname=parcelmaster_taxpayname,
            parcelmaster_taxpayname2=parcelmaster_taxpayname2,
            parcelMaster_taxpaystreetaddr=parcelMaster_taxpaystreetaddr,
            parcelmaster_taxpaycity=parcelmaster_taxpaycity,
            parcelmaster_taxpaystate=parcelmaster_taxpaystate,
            parcelmaster_taxpayzip=parcelmaster_taxpayzip,
            parcels_propclass=parcels_propclass,
            parcels_oldprop=parcels_oldprop,
            parcels_propstatus=parcels_propstatus,
            parcelmaster_exempt=parcelmaster_exempt,
            parcels_prevexemptcode=parcels_prevexemptcode,
            parcels_specialactscode=parcels_specialactscode,
            memoryfieldstable_assessmentyear=memoryfieldstable_assessmentyear,
            memoryfieldstable_previousassessmentyear=memoryfieldstable_previousassessmentyear,
            parcelreadonly_mborass1=parcelreadonly_mborass1,
            parcelreadonly_mborass2=parcelreadonly_mborass2,
            parcelreadonly_mborsev1=parcelreadonly_mborsev1,
            parcelreadonly_mborsev2=parcelreadonly_mborsev2,
            parcelreadonly_mbortax1=parcelreadonly_mbortax1,
            parcelreadonly_mbortax2=parcelreadonly_mbortax2,
            parcelmaster_specialnote=parcelmaster_specialnote,
            parcels_usecode=parcels_usecode,
            parcelmaster_vacant=parcelmaster_vacant,
            parcelmaster_lastsaleprice=parcelmaster_lastsaleprice,
            parcelmaster_lastsaledate=parcelmaster_lastsaledate,
            parcelmaster_cib_numcib=parcelmaster_cib_numcib,
            parcelmaster_cib_yearbuilt=parcelmaster_cib_yearbuilt,
            parcelmaster_cib_floorarea=parcelmaster_cib_floorarea,
            parcelmaster_resb_numresb=parcelmaster_resb_numresb,
            parcelmaster_resb_yearbuilt=parcelmaster_resb_yearbuilt,
            parcelmaster_resb_groundarea=parcelmaster_resb_groundarea,
            parcelmaster_totalacres=parcelmaster_totalacres,
            parcels_squarefootage=parcels_squarefootage,
            parcelmaster_frontage=parcelmaster_frontage,
            parcelmaster_avdepth=parcelmaster_avdepth,
            parcelmaster_landvalue=parcelmaster_landvalue,
            parcelmaster_landmap=parcelmaster_landmap,
            parcelmaster_namechgdate=parcelmaster_namechgdate,
            parcelmaster_relatedpnum=parcelmaster_relatedpnum,
            parcelmaster_xcord=parcelmaster_xcord,
            parcelmaster_ycord=parcelmaster_ycord,
            parcels_mapnum=parcels_mapnum,
            neighborhoods_neighcode=neighborhoods_neighcode,
            parcelmaster_block=parcelmaster_block,
            parcelmaster_sub=parcelmaster_sub,
            parcelmaster_liberpage=parcelmaster_liberpage,
            parcelreadonly_legaldescription=parcelreadonly_legaldescription,
            parcels_usernum=parcels_usernum,
            parcelmaster_ownername1=parcelmaster_ownername1)

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

            datareader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            row_data = []
            BATCHSIZE = 2500
            for row in datareader:

                if first_line:
                    first_line = False
                else:

                    # row = self.parse_row(row)
                    # row.validate()
                    # row.save()

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
