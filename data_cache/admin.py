from django.contrib import admin

from .models import DataCredential, DataSource, DataValue


class DataCredentialAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['username', 'password', 'referer', 'url']}),
    ]
    list_display = ('username', 'password', 'referer', 'url')
    list_filter = ['url']
    list_editable = ['password', 'referer', 'url']
    search_fields = ['url']
    ordering = ['url']

admin.site.register(DataCredential, DataCredentialAdmin)

class DataSourceAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'url', 'credentials']}),
    ]
    list_display = ('name', 'url', 'credentials')
    list_filter = ['url']
    list_editable = ['url', 'credentials']
    search_fields = ['url']
    ordering = ['url']

admin.site.register(DataSource, DataSourceAdmin)