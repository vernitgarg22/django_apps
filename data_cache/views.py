import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from cod_utils import util
from cod_utils import security
from cod_utils.cod_logger import CODLogger
from cod_utils.messaging import MsgHandler
from cod_utils.util import get_parcel_id

from data_cache.models import DataSet, DataSource, DataValue, DataDescriptor, DataCitySummary


@api_view(['POST'])
def add_url(request):
    """
    Creates a data_source object for the given url, in the data set 'url_cache', if one doesn't already exist,
    refreshes the data for it, if necessary, and returns the result.
    """

    # Only allow certain servers to call this endpoint
    if security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    url = request.data.get('url')
    if not url:
        return Response({ "error": "url is required" }, status.HTTP_400_BAD_REQUEST)

    data_set, created = DataSet.objects.get_or_create(name='url_cache')

    # Create a data source for this url.
    data_source_name = "url_cache_{}".format(data_set.datasource_set.count())
    data_source, created = DataSource.objects.get_or_create(name=data_source_name, url=url, data_set=data_set)

    # Retrieve the data values for this data set
    try:
        data = data_set.get(data_source_name=data_source_name)
    except:
        data = None

    # Do correct error handling if not found
    if not data:
        return Response({ "error": "No data received" }, status.HTTP_404_NOT_FOUND)

    # add a key to the response, which caller can use to retrieve this cached data source.
    data['key'] = data_source_name

    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def add_user_cache(request):
    """
    Creates a data_source object for the given piece of data, in the data set 'data_cache', if one doesn't already exist,
    refreshes the data for it, if necessary, and returns the result.  The key name should be passed as well.
    """

    # Only allow certain servers to call this endpoint
    if security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    data = request.data.get('data')
    if not data:
        return Response({ "error": "data is required" }, status.HTTP_400_BAD_REQUEST)

    key = request.data.get('key')
    if not key:
        return Response({ "error": "key is required" }, status.HTTP_400_BAD_REQUEST)

    data_set, created = DataSet.objects.get_or_create(name='user_cache')

    # Create a data source for this url.
    data_source_name = "user_cache_{}".format(key)
    data_source, created = DataSource.objects.get_or_create(name=data_source_name, data_set=data_set)

    # Create the data value for this data source.
    data_value, created = DataValue.objects.get_or_create(data_source=data_source)
    data_value.data = json.dumps(data)
    data_value.save()

    # Retrieve the data values for this data set
    try:
        data = data_set.get(data_source_name=data_source_name)
    except:
        data = None

    # Do correct error handling if not found
    if not data:
        return Response({ "error": "No data received" }, status.HTTP_404_NOT_FOUND)

    # add a key to the response, which caller can use to retrieve this cached data source.
    data['key'] = data_source_name

    return Response(data, status=status.HTTP_201_CREATED)


class SimpleJSONCache():

    cache = {}

    def get(name):

        return SimpleJSONCache.cache.get(name, {})

    def set(name, data):

        SimpleJSONCache.cache[name] = data

    def clear_all():

        SimpleJSONCache.cache = {}


def get_data_impl(name, param=None, path=None, force_refresh=False):

    data_source_name = None

    # Parse parcel ids when necessary
    if param:
        if name in [ 'url_cache', 'user_cache' ]:
            data_source_name = param
            param = None
        else:
            param = get_parcel_id(path, 3)

    data = {}
    if not force_refresh and not param:
        data = SimpleJSONCache.get(name)

    if not data:

        # Retrieve the data set
        try:
            data_set = DataSet.objects.get(name=name)
        except ObjectDoesNotExist:
            return Response({ "error": "Data set does not exist" }, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the data values for this data set
        try:
            data = data_set.get(data_source_name=data_source_name, param=param)
        except:
            data = None

        # Do correct error handling if not found
        if not data:
            if param:
                return Response({ "error": "Data value {} not found".format(param) }, status.HTTP_404_NOT_FOUND)
            else:
                return Response({ "error": "Data set {} not available".format(name) }, status.HTTP_503_SERVICE_UNAVAILABLE)

        SimpleJSONCache.set(name, data)

    return Response(data)


@api_view(['GET'])
def get_data(request, name, param=None):
    """
    Returns data cached for the given data source, updating the data whenever necessary.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    return get_data_impl(name=name, param=param, path=request.path)


@api_view(['POST'])
def refresh_cache(request):
    """
    Rebuilds data set cache.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    for data_set in DataSet.objects.all():
        get_data_impl(name=data_set.name, force_refresh=True)

    return Response({}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_city_data_summaries(request, param=None):
    """
    Returns list of data sets for overall 'city data summary' view.
    """

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    content = { "terms": {}, "summaries": [] }

    # add all terms
    for term in DataDescriptor.objects.all():
        if not content["terms"].get(term.descriptor_type):
            content["terms"][term.descriptor_type] = []
        content["terms"][term.descriptor_type].append(term.value)

    # add all summaries
    for summary in DataCitySummary.objects.all():

        summary_json = summary.json()
        if summary_json.get("data_set"):
            data_set = summary_json["data_set"]
            url = reverse("data_cache:data-set", args=[data_set], request=request)
            summary_json['url'] = url

        content["summaries"].append(summary_json)

    return Response(content)
