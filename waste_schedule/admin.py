from django.contrib import admin

from .models import ScheduleException


class ScheduleExceptionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['service_type', 'normal_day', 'rescheduled_day', 'reason', 'note']}),
    ]
    list_display = ('service_type', 'normal_day', 'rescheduled_day', 'reason', 'note')
    list_filter = ['service_type']
    # list_editable = ['service_type', 'normal_day', 'rescheduled_day', 'reason', 'note']
    search_fields = ['reason', 'note']
    ordering = ['normal_day', 'service_type']


admin.site.register(ScheduleException, ScheduleExceptionAdmin)
