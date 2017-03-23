from django.contrib import admin
from django.forms import Textarea

from .models import ScheduleChange, ScheduleDetail


class ScheduleChangeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['service_type', 'waste_area', 'normal_day', 'rescheduled_day', 'reason', 'note']}),
    ]
    list_display = ('waste_area', 'service_type', 'normal_day', 'rescheduled_day', 'reason', 'note')
    list_filter = ['service_type', 'waste_area']
    list_editable = ['waste_area', 'normal_day', 'rescheduled_day', 'reason', 'note']
    search_fields = ['reason', 'note']
    ordering = ['normal_day', 'service_type']


class ScheduleDetailAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['detail_type', 'service_type', 'description', 'normal_day', 'new_day', 'note', 'waste_area_ids']}),
    ]
    list_display = ('detail_type', 'service_type', 'description', 'normal_day', 'new_day', 'note', 'waste_area_ids')
    list_filter = ['detail_type', 'service_type']
    list_editable = ['detail_type', 'service_type', 'description', 'normal_day', 'new_day', 'note', 'waste_area_ids']
    # search_fields = ['reason', 'note']
    ordering = ['normal_day', 'new_day']

    # formfield_overrides = {
    #         models.TextField: {'widget': Textarea(
    #                            attrs={'rows': 1,
    #                                   'cols': 200,
    #                                   'style': 'height: 1em;'})},
    #     }


# admin.site.register(ScheduleDetail, ScheduleDetailAdmin)
admin.site.register(ScheduleChange, ScheduleChangeAdmin)