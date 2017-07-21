import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import Image, ImageMetadata


def clean_string(buffer):
    """
    Trim quotes from start and end of string
    """
    if len(buffer) >= 2 and buffer[0] == '"' and buffer[-1] == '"':
        return buffer[1:-1]
    else:
        return buffer


def clean_decimal(buffer):
    return Decimal(clean_string(buffer))


class Command(BaseCommand):
    help = """
        Use this to import image metadata from a csv file, e.g.,
        python manage.py import_image_metadata file_path
        python manage.py import_image_metadata survey_20170720.csv"""

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the csv file containing the image metadata")

    def handle(self, *args, **options):

        file_path = options['file_path']
        first_line = True
        files={}

        with open(file_path, newline='') as csvfile:
            datareader = csv.reader(csvfile, quotechar='|')
            for row in datareader:

                if first_line:
                    first_line = False
                else:

                    # print(', '.join(row))

                    # 0           1           2           3           4           5           6           7           8           9           10          11      12
                    # filepath    filename    longitude   latitude    altitude    gps_date    img_date    parcelno    house_numb  street_nam  street_typ  zipcode common_name

                    filename = clean_string(row[1])
                    parcel_id = clean_string(row[7])
                    created_at = datetime.strptime(clean_string(row[5]), "%Y:%m:%d %H:%M:%S")
                    path = clean_string(row[0])
                    subdir = path.split('/')[-2]
                    latitude = clean_decimal(row[3])
                    longitude = clean_decimal(row[2])
                    altitude = clean_decimal(row[4])

                    house_number = clean_string(row[8])
                    street_name = clean_string(row[9])
                    street_type = clean_string(row[10])
                    zipcode = clean_string(row[11])
                    common_name = clean_string(row[12])

                    file_path = subdir + '/' + filename

                    # print(parcel_id + ' - ' + file_path)

                    if not files.get(file_path):

                        prev_meta = ImageMetadata.objects.filter(image__file_path=file_path)
                        img_meta = None
                        if prev_meta:

                            img_meta = prev_meta[0]
                            img_meta.latitude=latitude;
                            img_meta.longitude=longitude;
                            img_meta.altitude=altitude
                            img_meta.save(force_update=True)

                        else:

                            img = Image(file_path=file_path)
                            img.save()

                            img_meta = ImageMetadata(image=img, parcel_id=parcel_id, created_at=created_at, 
                                            house_number=house_number, street_name=street_name, street_type=street_type, zipcode=zipcode, common_name=common_name, 
                                            latitude=latitude, longitude=longitude, altitude=altitude)
                            img_meta.save()

                        files[file_path] = True

                        # print(img_meta)