from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from data_cache.models import DataSource


class Command(BaseCommand):
    help = """
        This command refreshes the data cache, e.g.,
        python manage.py refresh_data_cache"""

    def handle(self, *args, **options):

        num_updated = 0
        data_sources = DataSource.objects.all()
        for data_source in data_sources:
            for data_value in data_source.datavalue_set.all():
                data_value.update()
                num_updated = num_updated + 1

        return "Updated {} data cache values".format(num_updated)
