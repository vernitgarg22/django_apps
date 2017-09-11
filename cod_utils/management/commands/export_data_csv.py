import csv
import importlib
import re
from pydoc import locate

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils import timezone


class Command(BaseCommand):
    help = """
        Use this to export survey data, e.g.,
        python manage.py export_data_csv database model
        python manage.py export_data_csv photo_survey Survey"""

    def add_arguments(self, parser):
        """
        Build command-line args.
        """
        parser.add_argument('application', type=str, help='Application to extract data from')
        parser.add_argument('database', type=str, help='Database to extract data from')
        parser.add_argument('model', type=str, help='Model to extract')
        parser.add_argument('output_file', type=str, help='File to output data to', default='')

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

        application = options['application']
        database = options['database']
        model = options['model']

        filename = database + '_' + model + '.csv'
        filename = options.get('output_file', filename)

        models = importlib.import_module('.models', application)
        klass = locate(application + '.models.' + model)
        if not klass:
            raise CommandError("Class {} not found".format(application + '.models.' + model))

        objects = klass.objects.using(database).all()

        lines = 0
        with open(filename, 'w', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(Command.get_header(klass))
            for obj in objects:
                try:
                    writer.writerow(self.get_data(obj))
                    lines = lines + 1
                except:
                    print('ignored a row for object {}'.format(obj))

        return "Wrote {} lines to {}".format(lines, filename)