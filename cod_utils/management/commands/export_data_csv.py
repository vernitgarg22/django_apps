import csv
import re
from pydoc import locate

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils import timezone

from photo_survey.models import Survey
from dnninternet.models import *


class Command(BaseCommand):
    help = """
        Use this to export survey data, e.g.,
        python manage.py export_data_csv database model
        python manage.py export_data_csv photo_survey Survey"""

    def add_arguments(self, parser):
        """
        Build command-line args.
        """
        parser.add_argument('database', type=str, help='Database to extract data from')
        parser.add_argument('model', type=str, help='Model to extract')

    @staticmethod
    def get_header(klass):
        """
        Get headers from the class object.
        """

        return [ field.name for field in klass._meta.local_fields ]

    @staticmethod
    def get_data_value(obj, field):
        """
        Extract the value for 'field' from the object.
        """

        value = obj.__getattribute__(field.name)

        if isinstance(value, models.Model):
            value = value.pk

        if type(value) == str:
            value = re.sub(r'[\r\n]', ' ', value)
            value = re.sub(r'&lt;', '<', value)
            value = re.sub(r'&gt;', '>', value)
        return value

    @staticmethod
    def get_data(obj):
        """
        Extract all django model fields from the object and return as list.
        """

        fields = type(obj)._meta.local_fields
        return [ Command.get_data_value(obj, field) for field in fields ]

    def handle(self, *args, **options):

        database = options['database']
        model = options['model']

        klass = locate(database + '.models.' + model)
        if not klass:
            raise CommandError("Class {} not found".format(database + '.models.' + model))

        objects = klass.objects.using(database).all()

        filename = database + '_' + model + '.csv'
        with open(filename, 'w', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(Command.get_header(klass))
            for obj in objects:
                try:
                    writer.writerow(self.get_data(obj))
                except:
                    print('ignored a row for object {}'.format(obj))
