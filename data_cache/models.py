import json
import requests

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

    def get(self):
        """
        Refreshes the data (if needed) and returns the datavalue object.
        """
        if self.datavalue_set.exists():
            data_value = self.datavalue_set.first()
        else:

            data_value = DataValue(data_source=self)
            data_value.update()

        return data_value

    def is_static(self):
        """
        Returns True if the data for this data source is 'static' and can only
        be set by hand.
        """

        return not self.url

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

    def save(self, *args, **kwargs):
        """
        Saves this DataValue object, updating 'updated' to current time.
        """

        self.updated = util.get_local_time()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def get_url(self):
        """
        Gets url, including auth token (if needed).
        """

        url = self.data_source.url

        token = None
        if self.data_source.credentials:
            success, token = self.data_source.credentials.create_auth_token()
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

    def update(self):
        """
        Update the data for this data value instance.
        """

        if self.data_source.is_static():
            return

        # Get the data
        url = self.get_url()
        r = requests.get(url)

        # Test success and attempt to parse
        if not status.is_success(r.status_code):    # pragma: no cover (exception-handling should prevent us from ever getting here)
            raise Exception("Data source {} not available".format(self.data_source.url))

        try:
            self.data = json.dumps(r.json())
            self.save()
        except json.decoder.JSONDecodeError:
            raise Exception("Invalid JSON received")

    def __str__(self):    # pragma: no cover (mostly for debugging)
        return self.data_source.name
