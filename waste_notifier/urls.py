from django.conf.urls import url

from . import views


app_name = 'waste_notifier'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe_notifications),
    url(r'^confirm/$', views.confirm_notifications),
    url(r'^send/(?P<date_name>[a-z]+)/$', views.send_notifications),
    url(r'^send/(?P<date_val>[0-9]{8})/$', views.send_notifications),
    url(r'^send/$', views.send_notifications),
    url(r'^route_info/$', views.get_route_info),
]
