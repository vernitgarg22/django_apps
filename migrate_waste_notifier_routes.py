#!/usr/bin/env python

import os
import csv
import django
import warnings

import pdb


def run_migration():

    from waste_notifier.models import Subscriber

    filename = "dpw_alerts_subscribers_updated.csv"
    row_num = 0

    with open(filename, newline='') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            subscriber = Subscriber.objects.get(id = row['id'])

            # # TODO remove this
            # subscriber = Subscriber.objects.get(phone_number = '9178428901')

            new_waste_area_ids = row['routeid19']
            lat = row['lat']
            lon = row['lon']


            # if new_waste_area_ids not in subscriber.waste_area_ids:

            #     print(f"{new_waste_area_ids} -> {subscriber.waste_area_ids}")


            # TODO un-comment this
            # subscriber.latitude = lat
            # subscriber.longitude = lon
            # subscriber.waste_area_ids = waste_area_ids
            # subscriber.save(force_update=True)

            row_num += 1
            if row_num % 250 == 0:

                print(f"Updated {row_num} subscribers")


if __name__ == "__main__":

    os.environ['DJANGO_HOME'] = os.getcwd()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    django.setup()

    warnings.filterwarnings(action="ignore", module='sql_server.pyodbc.operations', lineno=45)

    run_migration()
