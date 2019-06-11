#!/usr/bin/env python

import csv
from waste_notifier.models import Subscriber
from waste_notifier.util import geocode_address, get_waste_area_ids


import pdb


pdb.set_trace()
    

filename = "subscriber_responses.csv"

with open(filename, newline='') as csvfile:

    # From,To,Body,Status,SentDate,ApiVersion,NumSegments,ErrorCode,AccountSid,Sid,Direction,Price,PriceUnit
    reader = csv.DictReader(csvfile)

    for row in reader:

        phone_number = row['From']
        subscribers = Subscriber.objects.filter(phone_number = phone_number)

        # What if subscriber not found?
        if not subscribers:


            pdb.set_trace()


            continue

        subscriber = subscribers[0]

        # Don't overwrite existing address
        if subscriber.address:

            continue

        # Geocode the address.
        street_address = row['Body']
        location, address = geocode_address(street_address=street_address)

        # What if no location was found?
        if not location:
            print(f"Address '{street_address}' could not be geocoded")
            sys.stdout.flush()

            continue

        # Lookup up the waste area id.
        waste_area_ids = get_waste_area_ids(location=location)
        if not waste_area_ids:


            pdb.set_trace()


            print(f"ERROR:  No waste area ids found for address '{street_address}'")
            sys.stdout.flush()

            continue


        if type(waste_area_ids) == list:
            waste_area_ids = ''.join( [ str(num) + ',' for num in waste_area_ids ] )

        # Update subscriber waste area id and save
        subscriber.waste_area_ids = waste_area_ids
        subscriber.save(force_update=True)
