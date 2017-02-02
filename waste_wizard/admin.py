from django.contrib import admin

from .models import WasteItem


class WasteItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['description', 'destination', 'notes', 'keywords']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('description', 'destination', 'notes', 'keywords')
    list_filter = ['description']
    search_fields = ['description', 'keywords']

admin.site.register(WasteItem, WasteItemAdmin)
