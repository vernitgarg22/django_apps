from django.conf.urls import url

from messenger import views

app_name = 'messenger'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe),
    url(r'^locations/$', views.get_locations),
    url(r'^locations/(?P<value>[0-9]+)/notifications/$', views.get_location_notifications),
    url(r'^clients/$', views.get_notifications),
    url(r'^clients/(?P<client_id>[0-9]+)/$', views.get_notifications),
    url(r'^clients/(?P<client_id>[0-9]+)/notifications/$', views.add_notification),
    url(r'^clients/(?P<client_id>[0-9]+)/notifications/(?P<notification_id>[0-9]+)/$', views.add_notification),
    url(r'^notifications/(?P<notification_id>[0-9]+)/messages/$', views.add_notification_message),
    url(r'^notifications/(?P<notification_id>[0-9]+)/messages/(?P<message_id>[0-9]+)/$', views.add_notification_message),
]
