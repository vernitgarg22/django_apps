from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.conf import settings

from data_cache.models import DataSource
from data_cache.views import get_data_impl


class Command(BaseCommand):
    help = """
        This command refreshes the data cache, e.g.,
        python manage.py refresh_data_cache"""

    def trace(self, value):
        self.stdout.write(value)
        self.stdout.flush()

    def refresh(self, data_source):
        """
        Refreshes the individual data source.
        """

        name = data_source.data_set.name if data_source.data_set else data_source.name

        self.trace("starting data source {}".format(name))

        try:
            data_source.refresh()
        except Exception as error:    # pragma: no cover (should not get here)
            print("Exception {} occurred refreshing {}".format(error, data_source))

        self.trace("refreshed data source {}".format(name))
        return "refreshed data set {}".format(name)

    def handle(self, *args, **options):

        TIMEOUT = 120

        # Get all data sources
        data_sources = [ data_source for data_source in DataSource.objects.all().order_by('name') ]
        results = []

        # Kick off all the data source refreshes
        if settings.RUNNING_UNITTESTS:
            # unit tests sqlite database cannot handle multiple threads
            for data_source in data_sources:
                self.refresh(data_source)
        else:    # pragma: no cover
            with ThreadPoolExecutor(max_workers=8) as executor:
                results = executor.map(self.refresh, data_sources, timeout=TIMEOUT)

        # Convert the results returned to a list just so we can
        # do list stuff to it (like call len() on it)
        results = [ result for result in results ]

        msg = "Updated {} data cache sources".format(len(results))
        self.trace(msg)

        return msg
