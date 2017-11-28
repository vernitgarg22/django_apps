from django.conf.urls import url

from . import views


app_name = 'waste_notifier'
urlpatterns = [
    url(r'^address/(?P<street_address>[-\w\ ]+)/$', views.get_address_service_info),
    url(r'^address/(?P<street_address>[-\w\ ]+)/(?P<today>[0-9]{8})/$', views.get_address_service_info),
    url(r'^subscribe/$', views.subscribe_notifications),
    url(r'^subscribe/address/$', views.subscribe_address),
    url(r'^confirm/$', views.confirm_notifications),
    url(r'^route_info/$', views.get_route_info),
]
