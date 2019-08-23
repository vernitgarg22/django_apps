from django.contrib import admin

from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerMessage, MessengerSubscriber


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
        (None, {'fields': ['messenger_client', 'phone_number', 'description']})
    ]
    list_display = ('messenger_client', 'phone_number', 'description')
    search_fields = ['phone_number']
    ordering = ['phone_number']

admin.site.register(MessengerPhoneNumber, MessengerPhoneNumberAdmin)


class MessengerNotificationAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['messenger_client', 'day', 'geo_layer_url', 'formatter']})
    ]
    list_display = ('messenger_client', 'day', 'geo_layer_url', 'formatter')
    list_filter = ['day']
    search_fields = []
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
