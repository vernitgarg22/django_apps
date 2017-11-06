from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cod_utils import util
from cod_utils import security
from cod_utils.cod_logger import CODLogger
from cod_utils.messaging import MsgHandler
from cod_utils.util import get_parcel_id

from data_cache.models import DataSet, DataSource, DataValue


@api_view(['POST'])
def add_url(request, url=None):
    """
    Creates a data_source object for the given url, in the data set 'url_cache', if one doesn't already exist,
    refreshes the data for it, if necessary, and returns the result.
    """

    if not url:
        url = request.path[27:]

    data_set, created = DataSet.objects.get_or_create(name='url_cache')

    data_source_name = "url_cache_{}".format(data_set.datasource_set.count())
    data_source = DataSource(name=data_source_name, url=url, data_set=data_set)
    data_source.save()

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


@api_view(['GET'])
def get_data(request, name, param=None):
    """
    Returns data cached for the given data source, updating the data whenever necessary.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if security.block_client(request):
        remote_addr = request.META.get('REMOTE_ADDR')
        MsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    data_source_name = None

    # Parse parcel ids when necessary
    if param:
        if name == 'url_cache':
            data_source_name = param
            param = None
        else:
            param = get_parcel_id(request.path, 3)

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

    return Response(data)
