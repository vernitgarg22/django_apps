from django.contrib import admin

from .models import ScheduleChange


class ScheduleChangeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['service_type', 'waste_area', 'normal_day', 'rescheduled_day', 'reason', 'note']}),
    ]
    list_display = ('waste_area', 'service_type', 'normal_day', 'rescheduled_day', 'reason', 'note')
    list_filter = ['service_type', 'waste_area']
    list_editable = ['waste_area', 'normal_day', 'rescheduled_day', 'reason', 'note']
    search_fields = ['reason', 'note']
    ordering = ['normal_day', 'service_type']


admin.site.register(ScheduleChange, ScheduleChangeAdmin)
