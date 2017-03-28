from operator import attrgetter
from itertools import chain

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import ScheduleDetail


@api_view(['GET'])
def get_schedule_details(request, format=None):
    """
    List details to the waste collection schedule for a waste area
    """
    if request.method != 'GET':
        raise Http404("Method not supported")

    # get details that apply citywide
    citywide_details = ScheduleDetail.objects.filter(waste_area_ids__exact='')

    # get id of the waste area requested
    wa_id = int(request.path_info.split('/')[3])

    # find waste schedule details for this waste area
    wa_details = ScheduleDetail.objects.filter(waste_area_ids__contains=wa_id)

    details = sorted(chain(citywide_details, wa_details), key=attrgetter('normal_day'))

    # build an array of json objects, one for each detail
    content = [detail.json() for detail in details]

    return Response(content)
