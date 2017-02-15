from .models import ScheduleException
from rest_framework import viewsets
from .serializers import ScheduleExceptionSerializer


class ScheduleExceptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScheduleExceptions to be viewed.
    TODO:
    - add date filtering
    - format json properly
    """
    queryset = ScheduleException.objects.all().order_by('normal_day')
    serializer_class = ScheduleExceptionSerializer
    http_method_names = ['get']
