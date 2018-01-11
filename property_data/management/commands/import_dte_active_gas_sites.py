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

    def parse_row(self, row):

        business_partner = row[0]
        contract_account = row[1]
        installation_number = row[2]
        contract_number = row[3]
        connection_object = row[4]
        premise = row[5]
        house_number = row[6]
        street = row[7]
        secondary_code = row[8]
        secondary_value = row[9]
        city = row[10]
        postal_code = row[11]

        return DTEActiveGasSite(business_partner=business_partner, contract_account=contract_account, installation_number=installation_number, 
            contract_number=contract_number, connection_object=connection_object, premise=premise, house_number=house_number,
            street=street, secondary_code=secondary_code, secondary_value=secondary_value, city=city, postal_code=postal_code,
            active_date=date.today())

    def handle(self, *args, **options):

        file_path = options['file_path']
        first_line = True
        verbose = False

        with open(file_path, newline='') as csvfile:

            datareader = csv.reader(csvfile, delimiter='\t')
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
