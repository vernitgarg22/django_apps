import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ScheduleException
from .serializers import ScheduleExceptionSerializer


def date_as_json(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

@api_view(['GET'])
def schedule_exception_list(request, format=None):
    """
    List changes to the waste collection schedule
    """
    if request.method == 'GET':
        exceptions = ScheduleException.objects.all().order_by('normal_day', 'service_type')
        content = []
        for exception in exceptions:
            content.append({
                "serviceType": exception.service_type,
                "normalDay": date_as_json(exception.normal_day),
                "rescheduledDay": date_as_json(exception.rescheduled_day),
                "reason": exception.reason,
                "note": exception.note,
            })
        return Response(content)