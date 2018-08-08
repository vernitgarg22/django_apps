from django.contrib import admin

from django.contrib import admin

from .models import Poll, Precinct


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'address', 'latitude', 'longitude', 'congress_rep_district', 'state_senate_district', 'state_rep_district', 'map_url', 'image_url']}),
    ]
    list_display = ('name', 'address', 'latitude', 'longitude', 'congress_rep_district', 'state_senate_district', 'state_rep_district', 'map_url', 'image_url')
    list_filter = ['name', 'address']
    list_editable = ['address', 'latitude', 'longitude', 'congress_rep_district', 'state_senate_district', 'state_rep_district', 'map_url', 'image_url']
    search_fields = ['name', 'address']
    ordering = ['name']

admin.site.register(Poll, PollAdmin)


class PrecinctAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['poll', 'number']}),
    ]
    list_display = ('poll', 'number')
    list_filter = []
    list_editable = ['number']
    search_fields = []
    ordering = ['number']

admin.site.register(Precinct, PrecinctAdmin)
