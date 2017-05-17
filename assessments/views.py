import json
from operator import attrgetter
from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.http import Http404

from assessments.models import Sales, ParcelMaster
from assessments import util


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


def filter_years_back(results, years_back):

    # TODO not sure why this blows up on me (for now
    # just filter manually)
    # date_min = datetime.now() - timedelta(days=5 * 365)
    # results = results.filter(saledate__gte=date_min)

    today = datetime.now()
    return [ result for result in results if today.year - result.saledate.year <= int(years_back) ]


@api_view(['GET'])
def get_sales_property(request, pnum=None, years_back=None, format=None):
    """
    Retrieve property info via parcel id (aka 'pnum')
    """

    # urls with dots are problematic: substitute underscores for dots in the url
    # (and replace underscores with dots here)
    pnum = pnum.replace('_', '.')

    # Search for parcels with the given parcel num
    # pnum = request.path_info.split('/')[2]
    results = Sales.objects.filter(pnum__iexact=pnum)

    # filter recent-years only?
    if years_back != None:
        results = filter_years_back(results, years_back)

    # if no results found, return 404
    if len(results) == 0:
        raise Http404("Parcel id " + pnum + " not found")

    return get_parcels(results)


@api_view(['GET'])
def get_sales_property_recent(request, pnum=None, format=None):
    """
    Retrieve property info via parcel id (aka 'pnum'), for recent years only
    """

    return get_sales_property(request, pnum=pnum, years_back=5, format=format)


@api_view(['GET'])
def get_sales_property_address(request, address=None, years_back=None, format=None):
    """
    Retrieve property info via address
    """

    # urls with dots are problematic: substitute underscores for dots in the url
    # (and replace underscores with dots here)
    address = address.replace('_', '.')

    # Search for parcels with the given parcel num
    # pnum = request.path_info.split('/')[2]
    results = Sales.objects.filter(addresscombined__contains=address)

    # filter recent-years only?
    if years_back != None:
        results = filter_years_back(results, years_back)

    # if no results found, return 404
    if len(results) == 0:
        raise Http404("Address " + address + " not found")

    return get_parcels(results)


@api_view(['GET'])
def get_sales_property_address_recent(request, address=None, format=None):
    """
    Retrieve property info via address, for recent years only
    """

    return get_sales_property_address(request, address=address, years_back=5, format=format)

@api_view(['GET'])
def get_parcel(request, pnum=None, format=None):
    """
    Return parcel data from the assessors dataset
    """

    # clean up the pnum
    pnum = util.clean_pnum(pnum)

    # excecute the search
    parcels = ParcelMaster.objects.filter(pnum__iexact=pnum)
    if len(parcels) == 0:
        raise Http404("Parcel id " + pnum + " not found")

    content = parcels[0].json()
    content['field_descriptions'] = util.get_parcel_descriptions()

    return Response(content)

@api_view(['GET'])
def get_parcel_ownership_groups(request, owners=None, format=None):
    """
    Return sets of parcels grouped by owner
    """

    # hardcode the owners, for own - TODO fix this
    owners = [ 'DETROIT LAND BANK AUTHORITY', 'CITY OF DETROIT-P&DD', 'MI LAND BANK FAST TRACK AUTH', 'HANTZ WOODLANDS LLC', 'TAXPAYER' ]

    # excecute the search
    parcels = ParcelMaster.objects.filter(ownername1__in=owners)
    if not any(parcels):
        raise Http404("Parcels not found")

    content = [ { "pnum": parcel.pnum, "address": parcel.propstreetcombined, "owner_name": parcel.ownername1 } for parcel in parcels ]

    return Response(content)
