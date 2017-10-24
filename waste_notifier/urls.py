from django.conf.urls import url

from . import views


app_name = 'waste_notifier'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe_notifications),
    url(r'^subscribe/address/$', views.subscribe_address),
    url(r'^confirm/$', views.confirm_notifications),
    url(r'^route_info/$', views.get_route_info),
]
