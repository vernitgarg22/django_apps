import json
from operator import attrgetter
from datetime import datetime, timedelta

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


def filter_years_back(results, years_back):

    # TODO not sure why this blows up on me (for now
    # just filter manually)
    # date_min = datetime.now() - timedelta(days=5 * 365)
    # results = results.filter(saledate__gte=date_min)

    today = datetime.now()
    return [ result for result in results if today.year - result.saledate.year < int(years_back) ]


@api_view(['GET'])
def get_sales_property(request, pnum=None, years_back=None, format=None):
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

    # filter recent-years only?
    if years_back != None:
        results = filter_years_back(results, years_back)

    if len(results) == 0:
        return Response({"pnum": pnum})
    # if len(results) == 0:
    #     raise Http404("Parcel id " + pnum + " not found")

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

    # strictly GET-only
    if request.method != 'GET':
        raise Http404("Method not supported")

    # urls with dots are problematic: substitute underscores for dots in the url
    # (and replace underscores with dots here)
    address = address.replace('_', '.')

    # Search for parcels with the given parcel num
    # pnum = request.path_info.split('/')[2]
    results = Sales.objects.using('eql').filter(addresscombined__contains=address)

    # filter recent-years only?
    if years_back != None:
        results = filter_years_back(results, years_back)

    if len(results) == 0:
        return Response({"address": address})
    # if len(results) == 0:
    #     raise Http404("Address " + address + " not found")

    return get_parcels(results)


@api_view(['GET'])
def get_sales_property_address_recent(request, address=None, format=None):
    """
    Retrieve property info via address, for recent years only
    """

    return get_sales_property_address(request, address=address, years_back=5, format=format)



# from assessments.models import Sales
# from datetime import datetime, timedelta
# from django.db.models import Q
# pnum='22084716.'
# results = Sales.objects.using('eql').filter(pnum__iexact=pnum)
# date_min = datetime.now() - timedelta(days=5 * 365)
# date_min = datetime.today() - timedelta(days=5 * 365)
# results = results.filter(saledate__gte=date_min)

# results = Sales.objects.using('eql').filter(id__iexact=3769164).filter(saledate__gte=date_min)
# results = Sales.objects.using('eql').filter(id__iexact=3769164).filter(saledate__gte=today)
# results = Sales.objects.using('eql').filter(id__iexact=3769164).filter(datetime.combine(date_min, time.min))


# Events = Event.objects.filter(Q(date=now.date(),time__gte=now.time())|Q(date__gt=now.date())).order_by('-date')
# results = Sales.objects.using('eql').filter(id__iexact=3769164).filter(Q(saledate__gte=date_min)

# results = Sales.objects.using('eql').filter(pnum__iexact=pnum).filter(saledate__year=2007)
# results = Sales.objects.using('eql').filter(saledate__year=2017)