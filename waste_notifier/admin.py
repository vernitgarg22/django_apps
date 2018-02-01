from django.contrib import admin

from .models import Subscriber


# Globally disable delete selected
admin.site.disable_action('delete_selected')


class SubscriberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['phone_number', 'waste_area_ids', 'status', 'address', 'comment', 'last_status_update']}),
        ('Advanced', { 'classes': ('collapse',), 'fields': ('service_type', 'latitude', 'longitude') }),
    ]
    list_display = ('phone_number', 'status', 'address', 'comment', 'last_status_update')
    list_filter = ['status']
    list_editable = ['status', 'address', 'comment']
    search_fields = ['phone_number', 'waste_area_ids', 'status', 'address', 'comment', 'service_type']
    ordering = ['-last_status_update']

admin.site.register(Subscriber, SubscriberAdmin)
