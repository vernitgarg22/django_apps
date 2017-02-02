from django.contrib import admin

from .models import WasteItem


class WasteItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['description', 'destination', 'notes', 'keywords']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('description', 'destination', 'notes', 'keywords')
    list_filter = ['destination']
    list_editable = ['destination', 'keywords', 'notes']
    search_fields = ['description', 'keywords']
    ordering = ['description']

admin.site.register(WasteItem, WasteItemAdmin)
