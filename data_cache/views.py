import json

from django.shortcuts import render

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

from data_cache.models import DataSource, DataValue


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

    # Parse parcel ids when necessary
    if param:
        param = get_parcel_id(request.path, 3)

    # Retrieve the data source
    try:
        data_source = DataSource.objects.get(name=name)
    except ObjectDoesNotExist:
        return Response({ "error": "Data source does not exist" }, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the data value for the source
    try:
        data_value = data_source.get(param=param)
    except:
        data_value = None

    # Do correct error handling if not found
    if not data_value:
        if param:
            return Response({ "error": "Data value {} not found".format(param) }, status.HTTP_404_NOT_FOUND)
        else:
            return Response({ "error": "Data source {} not available".format(data_source.url) }, status.HTTP_503_SERVICE_UNAVAILABLE)

    # Return the data
    data = json.loads(data_value.data) if data_value and data_value.data else {}

    return Response( { "data": data, "updated": util.date_json(data_value.updated) })
