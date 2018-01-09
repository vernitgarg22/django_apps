import json
import requests

from django.conf import settings
from django.db import models
from rest_framework import status
from rest_framework.response import Response

from cod_utils import util


class DataSet(models.Model):
    """
    Represents a particular data set that has been cached.
    """

    app_label = 'data_cache'

    name = models.CharField('Name', max_length=64, db_index=True)

    @staticmethod
    def add_data_json(data, json):
        """
        Add the json object to the data.
        """

        if data.get("data"):

            if type(data.get("data")) == list:
                data["data"].extend(json)
            else:
                data["data"].update(json)
        else:
            data["data"] = json

    def get(self, data_source_name=None, param=None):
        """
        Refresh this dataset (if needed) and returns the datavalue objects.
        """

        data = {}

        updated = None

        data_sources = self.datasource_set.filter(name=data_source_name) if data_source_name else self.datasource_set.all()

        # combine the strings into 1 json object
        for data_source in data_sources:

            data_value = data_source.get(param)
            if data_value and data_value.data:
                json_curr = json.loads(data_value.data)
                self.add_data_json(data, json_curr)

                if not updated or data_value.updated < updated:
                    updated = data_value.updated

        if updated:
            data["updated"] = util.date_json(data_value.updated)

        return data

    @staticmethod
    def is_success(response):
        """
        Returns False if the response status code is not in the http success range (200-299) or
        if a gis service has returned a status code in the json that is not in the http success range.
        """

        data = response.json()
        gis_status_code = data.get("error", {}).get("code", 200) if type(data) is dict else 200
        return status.is_success(response.status_code) and status.is_success(gis_status_code)

    def __str__(self):    # pragma: no cover (mostly for debugging)
        return self.name


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
        return self.url


class DataSource(models.Model):
    """
    Represents a source of data needing to be cached.
    """

    app_label = 'data_cache'

    name = models.CharField('Name', max_length=64, unique=True, db_index=True)
    url = models.CharField('Data Source URL', max_length=3000, null=True, blank=True)
    data_set = models.ForeignKey(DataSet, null=True, blank=True)
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

        # Get the data
        url = self.get_url()
        r = requests.get(url)

        # Test success and attempt to parse
        if not DataSet.is_success(r):    # pragma: no cover (exception-handling should prevent us from ever getting here)
            raise Exception("Data source {} not available".format(self.name))

        data = r.json()
        if self.is_multiple():

            # keep a dict of all previous data values
            prev_data_values = { data_value.param : data_value for data_value in self.datavalue_set.all() }

            for idx, sub_data in enumerate(data[self.data_parse_path]):

                sub_data_tmp = sub_data
                for data_id_key in self.data_id_parse_path.split('/'):
                    sub_data_tmp = sub_data_tmp[data_id_key]

                param = str(sub_data_tmp)
                data_value, created = self.datavalue_set.get_or_create(param=param)

                data_value.data = json.dumps(sub_data)
                data_value.save(force_update=True)

                # removing each item from previous dict as it gets updated
                if prev_data_values.get(param):
                    del prev_data_values[param]

                if settings.RUNNING_UNITTESTS and idx == 100:
                    break

            # delete any 'orphans' at the end?
            for data_value in prev_data_values.values():
                data_value.delete()

        else:

            if self.datavalue_set.exists():
                data_value = self.datavalue_set.first()
            else:
                data_value = DataValue(data_source=self)
            data_value.data = json.dumps(data)
            data_value.save()

    def get(self, param=None):
        """
        Refreshes the data (if needed) and returns the datavalue objects.
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
                raise Exception("Authentication failed on credential {}".format(self.credentials))

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

        if self.data:
            try:
                json.loads(self.data)
            except json.decoder.JSONDecodeError:
                raise Exception("Data is not valid json")

        self.updated = util.get_local_time()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def __str__(self):    # pragma: no cover (mostly for debugging)
        return self.data_source.name


class DataDescriptor(models.Model):
    """
    Represents terms to describe data (e.g., categorize department that the dataset belongs to).
    """

    descriptor_type = models.CharField('Descriptor type', max_length=64)
    value = models.CharField('value', max_length=64)

    def json(self):
        """
        Returns json describing this descriptor.
        """

        return {
            "type": self.descriptor_type,
            "value": self.value,
        }


class DataCitySummary(models.Model):
    """
    Represents DataSets belonging to the 'city info' overview of important
    stats for the mayor's office.
    """

    app_label = 'data_cache'

    name = models.CharField('name', max_length=64)
    description = models.CharField('description', max_length=1024)

    data_set = models.ForeignKey(DataSet, null=True, blank=True)
    url = models.CharField('url', max_length=2056, null=True, blank=True)
    credentials = models.ForeignKey(DataCredential, null=True, blank=True)

    descriptor = models.ForeignKey(DataDescriptor, null=True, blank=True)

    def json(self):
        """
        Returns json describing the DataCitySummary object.
        """

        return {
            "name": self.name,
            "description": self.description,
            "data_set": self.data_set.name if self.data_set else None,
            "url": self.url,
            "credentials": self.credentials,
            "descriptor": self.descriptor.json() if self.descriptor else {}
        }

    class Meta:    # pragma: no cover
        ordering = ["name"]
        verbose_name_plural = "data city summaries"
