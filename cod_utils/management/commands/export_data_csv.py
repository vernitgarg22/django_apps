import csv
import importlib
import json
import re
from pydoc import locate

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils import timezone


class Command(BaseCommand):
    help = """
        Use this to export survey data, e.g.,
        python manage.py export_data_csv app database model output_file
        python manage.py export_data_csv app photo_survey Survey survey.csv"""

    def add_arguments(self, parser):
        """
        Build command-line args.
        """
        parser.add_argument('application', type=str, help='Application to extract data from')
        parser.add_argument('database', type=str, help='Database to extract data from')
        parser.add_argument('model', type=str, help='Model to extract')
        parser.add_argument('output_file', type=str, help='File to output data to', default='')
        parser.add_argument('--dedupe_key', default=None, help="Field to use for de-duping")
        parser.add_argument('--order_by', default=None, help="Field to order by")
        parser.add_argument('--query_params', default=None, help='JSON key value query params, e.g., {"detail_type": "info"}')

    @staticmethod
    def get_header(klass):
        """
        Get headers from the class object.
        """

        return [ field.name for field in klass._meta.local_fields ]

    def get_data_value(self, obj, field):
        """
        Extract the value for 'field' from the object.
        """

        value = obj.__getattribute__(field.name)
        if type(field) == models.ForeignKey:
            if value:
                value = value.pk
            else:

                related = type(obj).objects.using(self.database).filter(pk=obj.pk).select_related(field.name)
                if related:
                    value = related.first().__getattribute__(field.name)
                else:
                    value = obj.pk

        # if type(field) == models.ForeignKey:
        #     klass = field.related_model()
        #     values = type(klass).objects.using(self.database).filter(pk=obj.pk)
        #     if values:
        #         value = values[0]
        #     else:
        #         value = obj.pk
        # else:
        #     value = obj.__getattribute__(field.name)

        if isinstance(value, models.Model):
            value = value.pk

        if type(value) == str:
            value = re.sub(r'[\r\n]', ' ', value)
            value = re.sub(r'&lt;', '<', value)
            value = re.sub(r'&gt;', '>', value)
        return value

    def get_data(self, obj):
        """
        Extract all django model fields from the object and return as list.
        """

        fields = type(obj)._meta.local_fields
        return [ self.get_data_value(obj, field) for field in fields ]

    def write_all(self, objects, writer):
        """
        Write all objects to output.
        """

        for obj in objects:
            try:
                writer.writerow(self.get_data(obj))
                self.lines = self.lines + 1
            except:    # pragma: no cover (should never get here)
                print('ignored a row for object {}'.format(obj))

    def dedupe(self, objects, key):
        """
        Dedupe objects, based on key.
        """

        dedupe_key = key
        deduped = { obj.__getattribute__(dedupe_key) : obj for obj in objects }
        return [ obj for key, obj in deduped.items() ]

    def handle(self, *args, **options):

        self.application = options['application']
        self.database = options['database']
        model = options['model']

        dedupe_key = options['dedupe_key']
        order_by = options['order_by']
        query_params = options['query_params']

        filename = self.database + '_' + model + '.csv'
        filename = options.get('output_file', filename)

        models = importlib.import_module('.models', self.application)
        klass = locate(self.application + '.models.' + model)
        if not klass:
            raise CommandError("Class {} not found".format(self.application + '.models.' + model))    # pragma: no cover (should never get here)

        objects = klass.objects.using(self.database).all()

        if query_params:
            query_params = json.loads(query_params)
            objects = objects.filter(**query_params)

        if order_by:
            if not dedupe_key:
                raise Command("'order_by' and 'dedupe_key' must both be provided")    # pragma: no cover (should never get here)
            objects = objects.order_by(dedupe_key, order_by)

        self.lines = 0

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:

            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(Command.get_header(klass))

            if dedupe_key:
                objects = self.dedupe(objects, dedupe_key)

            self.write_all(objects, writer)

        return "Wrote {} lines to {}".format(self.lines, filename)