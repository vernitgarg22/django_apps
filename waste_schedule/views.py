from .models import ScheduleException
from rest_framework import viewsets
from .serializers import ScheduleExceptionSerializer


class ScheduleExceptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScheduleExceptions to be viewed or edited.
    TODO remove ability to edit(?)
    """
    queryset = ScheduleException.objects.all().order_by('normal_day')
    serializer_class = ScheduleExceptionSerializer
