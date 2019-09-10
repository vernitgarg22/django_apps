from django.contrib import admin

from messenger.models import *


class MessengerClientAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'description', 'confirmation_message']})
    ]
    list_display = ('name', 'description', 'confirmation_message')
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']

admin.site.register(MessengerClient, MessengerClientAdmin)


class MessengerPhoneNumberAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['messenger_client', 'phone_number', 'description', 'number_type']})
    ]
    list_display = ('messenger_client', 'phone_number', 'description', 'number_type')
    search_fields = ['phone_number']
    ordering = ['number_type', 'phone_number']

admin.site.register(MessengerPhoneNumber, MessengerPhoneNumberAdmin)


class MessengerLocationAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['location_type', 'prefix', 'value']})
    ]
    list_display = ('location_type', 'prefix', 'value')
    list_filter = ['location_type']
    search_fields = []
    ordering = ['location_type', 'value']

admin.site.register(MessengerLocation, MessengerLocationAdmin)


class MessengerNotificationAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['messenger_client', 'locations', 'day', 'geo_layer_url', 'formatter']})
    ]
    list_display = ('messenger_client', 'day', 'geo_layer_url', 'formatter')
    list_filter = ['day']
    search_fields = ['locations']
    ordering = ['day']

admin.site.register(MessengerNotification, MessengerNotificationAdmin)


class MessengerMessageAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['messenger_notification', 'lang', 'message']})
    ]
    list_display = ('messenger_notification', 'lang', 'message')
    list_filter = ['lang']
    search_fields = []
    ordering = []

admin.site.register(MessengerMessage, MessengerMessageAdmin)


class MessengerSubscriberAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['messenger_client', 'phone_number', 'status', 'address', 'lang']}),
        ('Advanced', { 'classes': ('collapse',), 'fields': ('latitude', 'longitude', 'created_at', 'last_status_update') }),
    ]
    list_display = ('phone_number', 'status', 'address', 'lang', 'latitude', 'longitude')
    list_filter = ['status']
    search_fields = ['phone_number', 'address']

admin.site.register(MessengerSubscriber, MessengerSubscriberAdmin)
