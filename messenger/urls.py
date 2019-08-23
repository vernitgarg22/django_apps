from django.conf.urls import url

from messenger import views

app_name = 'messenger'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe),
    url(r'^notifications/$', views.add_notification),
    url(r'^notifications/(?P<client_id>[0-9]+)/$', views.get_notifications),
    url(r'^notifications/(?P<notification_id>[0-9]+)/messages/$', views.add_notification_message),
    url(r'^notifications/(?P<notification_id>[0-9]+)/messages/(?P<message_id>[0-9]+)/$', views.add_notification_message),
]
