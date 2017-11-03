from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from data_cache.models import DataSource


class Command(BaseCommand):
    help = """
        This command refreshes the data cache, e.g.,
        python manage.py refresh_data_cache"""

    def handle(self, *args, **options):

        data_sets = set()
        data_sources = DataSource.objects.all()
        for data_source in data_sources:

            data_source.refresh()
            name = data_source.data_set.name if data_source.data_set else data_source.name
            data_sets.add(name)

            self.stdout.write("refreshed data set {}".format(name))
            self.stdout.flush()

        return "Updated {} data cache values".format(len(data_sets))
