import csv
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from data_cache.models import DTEActiveGasSite


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
        Use this to import tab-delimited dte active gas site data.

        Note:  Data will get loaded with today's date added.

        e.g.,
        python manage.py import_dte_active_gas_sites <input_file>
        python manage.py import_dte_active_gas_sites """

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the input file containing the data")

    def trace(self, value):
        self.stdout.write(value)
        self.stdout.flush()

    def clean_bigint(value):
        pos = value.find('.')
        if pos >= 0:
            value = value[0: pos]
        return value

    def parse_row(self, row):

        ignored = row[0]
        business_partner = row[1]
        contract_account = row[2]
        installation_number = Command.clean_bigint(row[3])
        contract_number = Command.clean_bigint(row[4])
        connection_object = Command.clean_bigint(row[5])
        premise = Command.clean_bigint(row[6])
        house_number = row[7]
        street = row[8]
        full_street_address = row[9]
        secondary_code = row[10]
        secondary_value = row[11]
        city = row[12]
        postal_code = row[13]
        ignored = row[14]
        parcel_id = row[15]

        return DTEActiveGasSite(business_partner=business_partner, contract_account=contract_account, installation_number=installation_number, 
            contract_number=contract_number, connection_object=connection_object, premise=premise, house_number=house_number,
            street=street, full_street_address=full_street_address, secondary_code=secondary_code, secondary_value=secondary_value, 
            city=city, postal_code=postal_code, active_date=date.today(), parcel_id=parcel_id)

    def handle(self, *args, **options):


        # # TODO remove this
        # DTEActiveGasSite.objects.all().delete()


        file_path = options['file_path']
        first_line = True
        verbose = False

        with open(file_path, newline='') as csvfile:

            datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
            row_data = []
            row_count = 0
            BATCHSIZE = 2500
            for row in datareader:

                if first_line:
                    first_line = False
                else:

                    site = self.parse_row(row)

                    if verbose:

                        self.trace("Loading site: " + str(site))
                        site.save()

                    else:

                        row_data.append(site)
                        if len(row_data) == BATCHSIZE:

                            DTEActiveGasSite.objects.bulk_create(row_data)
                            row_count = row_count + len(row_data)
                            self.trace("{} rows imported".format(row_count))
                            row_data = []

                            # if row_count >= 265000:
                            #     verbose = True

            if row_data:
                DTEActiveGasSite.objects.bulk_create(row_data)
                row_count = row_count + len(row_data)

            self.trace("Finished:  {} rows imported".format(row_count))
