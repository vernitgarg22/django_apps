from operator import attrgetter
from itertools import chain
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import ScheduleDetail


def check_month_val(year, month, day):
    if not day:
        return False
    if year:
        if day.year != int(year):
            return False
    if month:
        if day.month != int(month):
            return False
    return True

def check_month(year, month, detail):
    if detail.detail_type == 'start-date' or detail.detail_type == 'end-date':
        return True
    return check_month_val(year, month, detail.normal_day) or check_month_val(year, month, detail.new_day)

def filter_month(year, month, details):
    return [ detail for detail in details if check_month(year, month, detail) ]

@api_view(['GET'])
def get_schedule_details(request, waste_area_ids=None, year=None, month=None, format=None):
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

    if month or year:
        citywide_details = filter_month(year, month, citywide_details)
        wa_details = filter_month(year, month, wa_details)

    # sort the different sets of results by 'normal_day'
    details = sorted(chain(citywide_details, wa_details), key=attrgetter('sort_value'))

    # build an array of json objects, one for each detail
    content = [detail.json() for detail in details]

    return Response(content)
