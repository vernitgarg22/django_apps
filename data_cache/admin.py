from django.contrib import admin

from .models import DataSet, DataCredential, DataSource, DataValue, DataDescriptor, DataCitySummary


class DataSetAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    list_display = ('name', )
    list_filter = ['name']
    list_editable = []
    search_fields = []
    ordering = ['name']

admin.site.register(DataSet, DataSetAdmin)


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
        (None, {'fields': ['name', 'url', 'credentials', 'data_set', 'data_parse_path', 'data_id_parse_path', 'socrata_where']}),
    ]
    list_display = ('name', 'url', 'credentials', 'data_set', 'data_parse_path', 'data_id_parse_path', 'socrata_where')
    list_filter = []
    list_editable = ['url', 'credentials', 'data_set', 'data_parse_path', 'data_id_parse_path', 'socrata_where']
    search_fields = ['name']
    ordering = ['name']

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


class DataDescriptorAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['descriptor_type', 'value']}),
    ]
    list_display = ('descriptor_type', 'value')
    list_filter = ['descriptor_type']
    list_editable = ['value']
    search_fields = ['descriptor_type']
    ordering = ['descriptor_type', 'value']

admin.site.register(DataDescriptor, DataDescriptorAdmin)


class DataCitySummaryAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'description', 'data_set', 'url', 'descriptor', 'credentials']}),
    ]
    list_display = ('name', 'description', 'data_set', 'url', 'descriptor', 'credentials')
    list_editable = ['description', 'data_set', 'url', 'descriptor', 'credentials']
    search_fields = ['name']

admin.site.register(DataCitySummary, DataCitySummaryAdmin)
