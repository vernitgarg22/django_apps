import json
from operator import attrgetter
from datetime import timedelta
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.http import HttpResponse
from django.http import Http404

from assessments.models import Sales, ParcelMaster, Sketch, BSAPARCELDATA

from assessments.models import Parcel, CaseMain
from assessments import util

from cod_utils.cod_logger import CODLogger
from cod_utils.util import get_parcel_id


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
    # date_min = timezone.now() - timedelta(days=5 * 365)
    # results = results.filter(saledate__gte=date_min)

    today = timezone.now()
    return [ result for result in results if today.year - result.saledate.year <= int(years_back) ]


@api_view(['GET'])
def get_sales_property(request, pnum=None, years_back=None, format=None):
    """
    Retrieve property info via parcel id (aka 'pnum')
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    pnum = get_parcel_id(request.path, 2)

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

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    return get_sales_property(request, pnum=pnum, years_back=5, format=format)


@api_view(['GET'])
def get_sales_property_address(request, address=None, years_back=None, format=None):
    """
    Retrieve property info via address
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

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

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    return get_sales_property_address(request, address=address, years_back=5, format=format)


@api_view(['GET'])
def get_parcel(request, pnum=None, format=None):
    """
    Return parcel data from the assessors dataset
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # clean up the pnum
    pnum = get_parcel_id(request.path, 3)

    # excecute the search
    parcels = BSAPARCELDATA.objects.filter(PARCELNO=pnum)
    if not parcels:
        raise Http404("Parcel id " + pnum + " not found")

    content = parcels[0].json_data()
    content['field_descriptions'] = util.get_parcel_descriptions()

    return Response(content)


@api_view(['GET'])
def get_images(request, pnum=None, format=None):
    """
    Retrieve all images for the given parcel.
    """

    # REVIEW TODO add frank's suggestions

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # clean up the pnum
    pnum = get_parcel_id(request.path, 2)
    sketch_data = Sketch.objects.filter(pnum=pnum).order_by('-date')
    content = []

    # REVIEW (TODO) remove the call to move_files() ...

    for sketch in sketch_data:

        content.append(sketch.get_json())

    return Response(content)


@api_view(['GET'])
def get_image(request, id, format=None):
    """
    Retrieve an image from the assessors database.
    """

    # REVIEW TODO add frank's suggestions


    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    sketches = Sketch.objects.filter(id=int(id))
    if not sketches:
        raise Http404("Sketch id " + id + " not found")

    sketch = sketches.first()

    return HttpResponse(sketch.imageData, content_type="image/jpg")


# @api_view(['GET'])
# def get_parcel_ownership_groups(request, owners=None, format=None):
#     """
#     Return sets of parcels grouped by owner
#     """


#     # cache_key = 'ownership_groups'
#     # cached_content = cache.get(cache_key, None)
#     # if cached_content:
#     #     return Response(cached_content)

#     # hardcode the owners, for own - TODO fix this
#     owners = [ 'DETROIT LAND BANK AUTHORITY', 'CITY OF DETROIT-P&DD', 'MI LAND BANK FAST TRACK AUTH', 'HANTZ WOODLANDS LLC', 'TAXPAYER' ]

#     # excecute the search
#     parcels = ParcelMaster.objects.filter(ownername1__in=owners)

#     content = [ { "pnum": parcel.pnum, "address": parcel.propstreetcombined, "owner_name": parcel.ownername1 } for parcel in parcels ]

#     # cache.set(cache_key, content, 60 * 60)

#     return Response(content)


class ParcelOwnershipGroupsView(APIView):

    def get(self, request, owners=None, format=None):
        """
        Return sets of parcels grouped by owner
        """

        CODLogger.instance().log_api_call(name=__name__, msg=request.path)

        # TODO get cache working?
        # cache_key = 'ownership_groups'
        # cached_content = cache.get(cache_key, None)
        # if cached_content:
        #     return Response(cached_content)

        # hardcode the owners, for own - TODO fix this
        owners = [ 'DETROIT LAND BANK AUTHORITY', 'CITY OF DETROIT-P&DD', 'MI LAND BANK FAST TRACK AUTH', 'HANTZ WOODLANDS LLC', 'TAXPAYER' ]

        # excecute the search
        parcels = ParcelMaster.objects.filter(ownername1__in=owners)

        content = [ { "pnum": parcel.pnum, "address": parcel.propstreetcombined, "owner_name": parcel.ownername1 } for parcel in parcels ]

        # cache.set(cache_key, content, 60 * 60)

        return Response(content)



@api_view(['GET'])
def get_rental_cases(request, pnum=None, format=None):
    """
    Return rental unit cases from tidemark (oracle)
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    # TODO need massive cleanup for tidemark pnums
    # clean up the pnum
    # pnum = util.clean_pnum(pnum)

    # excecute the search
    casemains = CaseMain.objects.filter(prc_parcel_no__prc_parcel_no__exact=pnum)
    if not casemains.exists():
        raise Http404("Parcel id " + pnum + " not found")

    content = [ casemain.json() for casemain in casemains ]

    return Response(content)
