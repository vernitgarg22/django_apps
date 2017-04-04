from django.contrib import admin

from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['phone_number', 'waste_area_ids', 'status']}),
    ]
    list_display = ('phone_number', 'waste_area_ids', 'status')
    list_filter = ['status', 'waste_area_ids']
    list_editable = ['phone_number', 'waste_area_ids', 'status']
    search_fields = ['phone_number', 'waste_area_ids', 'status']
    ordering = ['status', 'waste_area_ids']

admin.site.register(Subscriber, SubscriberAdmin)
