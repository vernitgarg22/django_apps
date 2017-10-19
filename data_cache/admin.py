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
        (None, {'fields': ['name', 'url', 'credentials', 'data_parse_path', 'data_id_parse_path']}),
    ]
    list_display = ('name', 'url', 'credentials', 'data_parse_path', 'data_id_parse_path')
    list_filter = ['url']
    list_editable = ['url', 'credentials', 'data_parse_path', 'data_id_parse_path']
    search_fields = ['url']
    ordering = ['url']

admin.site.register(DataSource, DataSourceAdmin)

class DataValueAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['data_source', 'data', 'updated', 'param']}),
    ]
    list_display = ('data_source', 'data', 'updated', 'param')
    list_filter = ['data_source']
    list_editable = ['data', 'updated']
    search_fields = ['data_source']
    ordering = ['data_source']

admin.site.register(DataValue, DataValueAdmin)
