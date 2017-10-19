import json
import requests

from django.conf import settings
from django.db import models
from rest_framework import status
from rest_framework.response import Response

from cod_utils import util


class DataCredential(models.Model):
    """
    Login credentials for a particular data source.
    """

    app_label = 'data_cache'

    username = models.CharField('Username', max_length=64)
    password = models.CharField('Password', max_length=64)
    referer = models.CharField('Referer', max_length=64)
    url = models.CharField('Authentication URL', max_length=256)

    def create_auth_token(self):
        """
        Gets an authentication token for the given set of credentials.
        """

        try:
            r = requests.post(self.url, data = { "username": self.username, "password": self.password })
            if status.is_success(r.status_code):
                return True, r.text
        except:
            pass

        return False, ''

    def __str__(self):    # pragma: no cover (mostly for debugging)
        return self.username


class DataSource(models.Model):
    """
    Represents a source of data needing to be cached.
    """

    app_label = 'data_cache'

    name = models.CharField('Name', max_length=64, unique=True, db_index=True)
    url = models.CharField('Data Source URL', max_length=1024, null=True, blank=True)
    credentials = models.ForeignKey(DataCredential, null=True, blank=True)
    data_parse_path = models.CharField('Data to extract', max_length=128, null=True, blank=True)
    data_id_parse_path = models.CharField('Data ID to extract', max_length=128, null=True, blank=True)

    def refresh(self):
        """
        Update all data values for this data source.
        """

        # Is the data for this data source set once, manually?
        if self.is_static():
            if not self.datavalue_set.exists():
                DataValue(data_source=self).save()
            return

        # TODO figure out a way to guarantee that any deleted items will not persist
        # keep a dict of all items, removing each item as it gets updated, then
        # delete any 'orphans' at the end?

        # Get the data
        url = self.get_url()
        r = requests.get(url)

        # Test success and attempt to parse
        if not status.is_success(r.status_code):    # pragma: no cover (exception-handling should prevent us from ever getting here)
            raise Exception("Data source {} not available".format(self.data_source.url))

        # TODO clean this up a bit?
        try:

            data = r.json()
            if self.is_multiple():

                for idx, sub_data in enumerate(data[self.data_parse_path]):

                    sub_data_tmp = sub_data
                    for data_id_key in self.data_id_parse_path.split('/'):
                        sub_data_tmp = sub_data_tmp[data_id_key]

                    data_value, success = self.datavalue_set.get_or_create(param=sub_data_tmp)

                    data_value.data = json.dumps(sub_data)
                    data_value.save(force_update=True)

                    if settings.RUNNING_UNITTESTS and idx == 100:
                        break

            else:

                if self.datavalue_set.exists():
                    data_value = self.datavalue_set.first()
                else:
                    data_value = DataValue(data_source=self)
                data_value.data = json.dumps(data)
                data_value.save()

        except json.decoder.JSONDecodeError:
            raise Exception("Invalid JSON received")

    def get(self, param=None):
        """
        Refreshes the data (if needed) and returns the datavalue object.
        """

        # Retrieve the data, if necessary
        if not self.datavalue_set.exists():
            self.refresh()

        # Now return the requested data_value
        if param:
            data_value = self.datavalue_set.filter(param=param).first()
        else:
            data_value = self.datavalue_set.first()

        return data_value

    def is_static(self):
        """
        Returns True if the data for this data source is 'static' and can only
        be set by hand.
        """

        return not self.url

    def is_multiple(self):
        """
        Returns True if there can be more than 1 data value for this data source.
        """

        return self.data_parse_path and self.data_id_parse_path

    def get_url(self):
        """
        Gets url, including auth token (if needed).
        """

        url = self.url

        token = None
        if self.credentials:
            success, token = self.credentials.create_auth_token()
            if False == success:
                raise Exception("Authentication failed")

        # Add auth token to url?
        if token:
            if url.find("?") < 0:
                url = url + "?"
            else:
                url = url + "&"
            url = url + "token={}".format(token)

        return url

    def __str__(self):    # pragma: no cover (mostly for debugging)
        return self.name


class DataValue(models.Model):
    """
    Stores data for each data source.
    """

    app_label = 'data_cache'

    data_source = models.ForeignKey(DataSource)
    data = models.TextField()
    updated = models.DateTimeField('Last time data was cached')
    param = models.CharField(max_length=128, blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):
        """
        Saves this DataValue object, updating 'updated' to current time.
        """

        self.updated = util.get_local_time()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def __str__(self):    # pragma: no cover (mostly for debugging)
        return self.data_source.name
