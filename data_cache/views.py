from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cod_utils.cod_logger import CODLogger
from cod_utils import util

from data_cache.models import DataSource, DataValue


@api_view(['GET'])
def get_data(request, name):
    """
    Returns data cached for the given data source, updating the data whenever necessary.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Retrieve the data source
    try:
        data_source = DataSource.objects.get(name=name)
    except ObjectDoesNotExist:
        return Response({ "error": "Data source does not exist" }, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the data value for the source
    try:
        data_value = data_source.get()
    except:
        return Response({ "error": "Data source {} not available".format(data_source.url) }, status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response( { "data": data_value.data, "updated": util.date_json(data_value.updated) })
