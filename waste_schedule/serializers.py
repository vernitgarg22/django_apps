from .models import ScheduleChange
from rest_framework import serializers


class ScheduleChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduleChange
        fields = ('service_type', 'normal_day', 'rescheduled_day', 'reason', 'note')
