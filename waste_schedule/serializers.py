from .models import ScheduleException
from rest_framework import serializers


class ScheduleExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduleException
        fields = ('service_type', 'normal_day', 'rescheduled_day', 'reason', 'note')
