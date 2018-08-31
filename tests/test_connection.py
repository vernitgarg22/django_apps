#!/usr/bin/env python

import os

import django
from django_apps import settings
from django.db import connection


model_map = {
    "Poll": "elections",
    "DataSet": "data_cache",
    "Faqs": "dnninternet",
    "Sales": "assessments",
    "Image": "photo_survey",
    "EscrowBalance": "property_data",
    "Subscriber": "waste_notifier",
}


def test_connections(debug):

    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    django.setup()

    settings.DEBUG = debug

    for class_name, module in model_map.items():

        mod = __import__(module + '.models', fromlist=[class_name])
        klass = getattr(mod, class_name)

        try:

            obj = klass.objects.first()

        except (django.db.utils.ProgrammingError, django.db.utils.InterfaceError) as err:

            print("Could not connect to database for {}.models.{}\nerror message:\n\n{}\n".format(module, class_name, err))


if __name__ == '__main__':

    for debug in [ True ]:
        test_connections(debug=debug)
