import json
from operator import attrgetter

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import Sales


import pdb


@api_view(['GET'])
def get_sales_property(request, format=None):
    """
    Retrieve property info via parcel id (aka 'pnum')
    """
    if request.method != 'GET':
        raise Http404("Method not supported")

    # Search for parcels with the given parcel num
    pnum = request.path_info.split('/')[2]
    results = Sales.objects.using('eql').filter(pnum__iexact=pnum)
    if len(results) == 0:
        raise Http404("Parcel id " + pnum + " not found")

    # Sort the parcels in reverse order by sale date
    parcels = sorted(results, key=attrgetter('saledate'), reverse=True)

    # return json for each parcel
    content = [parcel.json() for parcel in parcels]
    return Response(content)
