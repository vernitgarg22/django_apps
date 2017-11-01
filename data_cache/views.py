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

from data_cache.models import DataSet, DataSource, DataValue


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

    # Retrieve the data set
    try:
        data_set = DataSet.objects.get(name=name)
    except ObjectDoesNotExist:
        return Response({ "error": "Data set does not exist" }, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the data values for this data set
    try:
        data = data_set.get(param=param)
    except:
        data = None

    # Do correct error handling if not found
    if not data:
        if param:
            return Response({ "error": "Data value {} not found".format(param) }, status.HTTP_404_NOT_FOUND)
        else:
            return Response({ "error": "Data set {} not available".format(name) }, status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(data)
