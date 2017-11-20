from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from data_cache.models import DataSource


class Command(BaseCommand):
    help = """
        This command refreshes the data cache, e.g.,
        python manage.py refresh_data_cache"""

    def refresh(self, data_source):
        """
        Refreshes the individual data source.
        """

        try:
            data_source.refresh()
        except Exception as error:    # pragma: no cover (should not get here)
            print("Exception {} occurred refreshing {}".format(error, data_source))

        name = data_source.data_set.name if data_source.data_set else data_source.name

        self.stdout.write("refreshed data source {}".format(name))
        self.stdout.flush()
        return "refreshed data set {}".format(name)

    def handle(self, *args, **options):

        # Get all data sources
        data_sources = [ data_source for data_source in DataSource.objects.all().order_by('name') ]
        results = []

        # Kick off all the data source refreshes
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(self.refresh, data_sources)

        # Convert the results returned to a list just so we can
        # do list stuff to it (like call len() on it)
        results = [ result for result in results ]

        return "Updated {} data cache sources".format(len(results))
