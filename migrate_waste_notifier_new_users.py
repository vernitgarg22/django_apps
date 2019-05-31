#!/usr/bin/env python

import os
import csv
import django
import warnings

import pdb


def run_migration():

    from waste_notifier.models import Subscriber
    from waste_notifier.util import geocode_address, get_waste_area_ids

    row_num = 0


    pdb.set_trace()
    

    subscribers = Subscriber.objects.filter(id__gte= 41801)
    for subscriber in subscribers:

        street_address = subscriber.address
        if not street_address:
            continue

        street_address = street_address.upper()
        location, address = geocode_address(street_address=street_address)

        # What if no location was found?
        if not location:
            print(f"Address '{street_address}' could not be geocoded")
            continue

        waste_area_ids = get_waste_area_ids(location=location)
        if not waste_area_ids:
            print(f"ERROR:  No waste area ids found for address '{street_address}'")
            return

        if type(waste_area_ids) == list:
            waste_area_ids = ''.join( [ str(num) + ',' for num in waste_area_ids ] )

        # TODO uncomment this
        # subscriber.waste_area_ids = waste_area_ids
        # subscriber.save(force_update=True)
    
        row_num += 1
        if row_num % 50 == 0:

            print(f"Updated {row_num} subscribers")


if __name__ == "__main__":

    os.environ['DJANGO_HOME'] = os.getcwd()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    django.setup()

    warnings.filterwarnings(action="ignore", module='sql_server.pyodbc.operations', lineno=45)

    run_migration()
