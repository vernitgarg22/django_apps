from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cod_utils import util
from cod_utils import security
from cod_utils.cod_logger import CODLogger
from cod_utils.util import get_parcel_id
from cod_utils.messaging import MsgHandler

from data_cache.models import DTEActiveGasSite
from property_data.models import EscrowBalance


@api_view(['GET'])
def get_dte_active_connection(request, parcel_id, param=None):
    """
    Returns data cached for the given data source, updating the data whenever necessary.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if security.block_client(request):    # pragma: no cover
        remote_addr = request.META.get('REMOTE_ADDR')
        SlackMsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    parcel_id = get_parcel_id(request.path, 4)

    if not DTEActiveGasSite.objects.filter(parcel_id=parcel_id).exists():
        raise Http404("No parcel " + parcel_id + " found with active connection")

    return Response({ "active": True })


@api_view(['GET'])
def get_escrow_data(request, item_num, param=None):
    """
    Returns escrow data for the given item num.
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # Only allow certain servers to call this endpoint
    if security.block_client(request):    # pragma: no cover
        remote_addr = request.META.get('REMOTE_ADDR')
        SlackMsgHandler().send_admin_alert("Address {} was blocked from subscribing waste alerts".format(remote_addr))
        return Response("Invalid caller ip or host name: " + remote_addr, status=status.HTTP_403_FORBIDDEN)

    # Only call via https...
    if not request.is_secure():
        return Response({ "error": "must be secure" }, status=status.HTTP_403_FORBIDDEN)

    balances = EscrowBalance.objects.filter(item_num=item_num)
    if not balances.exists():
        raise Http404("No escrow data found for item number " + str(item_num))

    return Response(balances.first().to_json())
