import json
from operator import attrgetter
from itertools import chain

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import ScheduleChange, ScheduleDetail, WasteArea
from .serializers import ScheduleChangeSerializer


def date_as_json(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

@api_view(['GET'])
def get_schedule_changes(request, format=None):
    """
    List changes to the waste collection schedule
    """
    if request.method == 'GET':

        all_wa = WasteArea.objects.get(id = WasteArea.ALL_WASTE_AREAS_ID)
        wa_id = int(request.path_info.split('/')[4])
        try:
            wa = WasteArea.objects.get(id = wa_id)
        except WasteArea.DoesNotExist:
            raise Http404("Waste area " + str(wa_id) + " not found")
        wa_changes = wa.schedulechange_set.all()
        all_wa_changes = all_wa.schedulechange_set.all()

        changes = sorted(chain(wa_changes, all_wa_changes), key=attrgetter('normal_day'))

        content = []
        for change in changes:
            content.append({
                "serviceType": change.service_type,
                "waste_area": change.waste_area.description,
                "waste_area_id": change.waste_area.id,
                "normalDay": date_as_json(change.normal_day),
                "rescheduledDay": date_as_json(change.rescheduled_day),
                "reason": change.reason,
                "note": change.note,
            })
        return Response(content)


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
