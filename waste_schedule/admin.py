from django.contrib import admin
from django.forms import Textarea

from .models import ScheduleChange, ScheduleDetail


class ScheduleDetailAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['detail_type', 'service_type', 'description', 'normal_day', 'new_day', 'note', 'waste_area_ids']}),
    ]
    list_display = ('detail_type', 'service_type', 'description', 'normal_day', 'new_day', 'note', 'waste_area_ids')
    list_filter = ['detail_type', 'service_type']
    list_editable = ['detail_type', 'service_type', 'description', 'normal_day', 'new_day', 'note', 'waste_area_ids']
    search_fields = ['reason', 'note']
    ordering = ['normal_day', 'new_day']

admin.site.register(ScheduleDetail, ScheduleDetailAdmin)
