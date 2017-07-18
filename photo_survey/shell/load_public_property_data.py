import csv

from photo_survey.models import PublicPropertyData


# from photo_survey.shell import load_public_property_data
# load_public_property_data.run_import('ocfo.csv')


FIELDNAMES=[ "parcelno", "propaddress", "propzip", "taxpayer1", "taxpayer2", "taxaddr", "taxcity", "taxstate", "taxzip", "project_co", "ownership_" ]


def run_import(csv_file_path):
    first_line = True
    files={}

    PublicPropertyData.objects.all().delete()

    with open(csv_file_path, newline='') as csvfile:
        datareader = csv.DictReader(csvfile, fieldnames=FIELDNAMES)
        row_count = 0
        for row in datareader:
            
            if first_line:
                first_line = False
            else:

                # print(', '.join(row))

                ownership = row.pop('ownership_')
                row['ownership'] = ownership

                data = PublicPropertyData(**row)
                data.save()

                row_count = row_count + 1
                if row_count % 1000 == 0:
                    print("{} rows exported ...".format(row_count))
