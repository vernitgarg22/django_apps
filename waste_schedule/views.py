from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ScheduleException
from .serializers import ScheduleExceptionSerializer


class ScheduleExceptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScheduleExceptions to be viewed.
    TODO:
    - add filtering by district and date
    - format json properly
    """
    queryset = ScheduleException.objects.all().order_by('normal_day')
    serializer_class = ScheduleExceptionSerializer
    http_method_names = ['get']


@api_view(['GET'])
def schedule_exception_list(request, format=None):
    """
    List changes to the waste collection schedule
    """
    if request.method == 'GET':
        exceptions = ScheduleException.objects.all()
        serializer = ScheduleExceptionSerializer(exceptions, many=True)
        return Response(serializer.data)
