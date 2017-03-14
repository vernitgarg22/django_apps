import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ScheduleChange
from .serializers import ScheduleChangeSerializer


def date_as_json(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

@api_view(['GET'])
def schedule_exception_list(request, format=None):
    """
    List changes to the waste collection schedule
    """
    if request.method == 'GET':
        changes = ScheduleChange.objects.all().order_by('normal_day', 'service_type')
        content = []
        for change in changes:
            content.append({
                "serviceType": change.service_type,
                "normalDay": date_as_json(change.normal_day),
                "rescheduledDay": date_as_json(change.rescheduled_day),
                "reason": change.reason,
                "note": change.note,
            })
        return Response(content)