from operator import attrgetter
from itertools import chain
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import ScheduleDetail


import pdb


@api_view(['GET'])
def get_schedule_details(request, waste_area_ids=None, month=datetime.now().month, format=None):
    """
    List details to the waste collection schedule for a waste area
    """
    if request.method != 'GET':
        raise Http404("Method not supported")

    # get details that apply citywide
    citywide_details = ScheduleDetail.objects.filter(waste_area_ids__exact='')

    wa_ids = [ int(wa_id) for wa_id in waste_area_ids.split(',') ]
    wa_details = ScheduleDetail.objects.none()

    # get waste schedule details for each waste area requested
    for wa_id in wa_ids:
        wa_details = wa_details | ScheduleDetail.objects.filter(waste_area_ids__contains=wa_id)

    # sort the different sets of results by 'normal_day'
    details = sorted(chain(citywide_details, wa_details), key=attrgetter('sort_value'))

    # build an array of json objects, one for each detail
    content = [detail.json() for detail in details]

    return Response(content)
