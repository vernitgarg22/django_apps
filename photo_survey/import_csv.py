import csv

from photo_survey.models import Image, ImageMetadata
from datetime import datetime


def clean_string(buffer):
    if len(buffer) >= 2:
        return buffer[1:-1]
    else:
        return ''


def run_import(csv_file_path):
    first_line = True
    files={}

    with open(csv_file_path, newline='') as csvfile:
        datareader = csv.reader(csvfile, quotechar='|')
        for row in datareader:
            
            if first_line:
                first_line = False
            else:

                # print(', '.join(row))

                filename = clean_string(row[0])
                parcel_id = clean_string(row[1])
                created_at = datetime.strptime(clean_string(row[2]), "%Y:%m:%d %H:%M:%S")
                path = clean_string(row[3])
                subdir = path.split('\\')[6]

                file_path = subdir + '/' + filename
                if not files.get(file_path):
                    img = Image(file_path=file_path)
                    img.save()
                    img_meta = ImageMetadata(image=img, parcel_id=parcel_id, created_at=created_at)
                    img_meta.save()

                    files[file_path] = True

                    # print(img_meta)