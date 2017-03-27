import json
from operator import attrgetter

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import Sales


def get_parcels(parcels):
    """
    Retrieve property info
    """

    # remove any parcels with null saledate
    parcels = [ parcel for parcel in parcels if parcel.saledate ]

    # Sort the parcels in reverse order by sale date
    parcels = sorted(parcels, key=attrgetter('saledate'), reverse=True)

    # return json for each parcel
    content = [parcel.json() for parcel in parcels]
    return Response(content)


@api_view(['GET'])
def get_sales_property(request, pnum=None, format=None):
    """
    Retrieve property info via parcel id (aka 'pnum')
    """

    # strictly GET-only
    if request.method != 'GET':
        raise Http404("Method not supported")

    # urls with dots are problematic: substitute underscores for dots in the url
    # (and replace underscores with dots here)
    pnum = pnum.replace('_', '.')

    # Search for parcels with the given parcel num
    # pnum = request.path_info.split('/')[2]
    results = Sales.objects.using('eql').filter(pnum__iexact=pnum)
    if len(results) == 0:
        return Response({"pnum": pnum})
    # if len(results) == 0:
    #     raise Http404("Parcel id " + pnum + " not found")

    return get_parcels(results)


@api_view(['GET'])
def get_sales_property_address(request, address=None, format=None):
    """
    Retrieve property info via address
    """

    # strictly GET-only
    if request.method != 'GET':
        raise Http404("Method not supported")

    # urls with dots are problematic: substitute underscores for dots in the url
    # (and replace underscores with dots here)
    address = address.replace('_', '.')

    # Search for parcels with the given parcel num
    # pnum = request.path_info.split('/')[2]
    results = Sales.objects.using('eql').filter(addresscombined__contains=address)
    if len(results) == 0:
        return Response({"address": address})
    # if len(results) == 0:
    #     raise Http404("Address " + address + " not found")

    return get_parcels(results)
