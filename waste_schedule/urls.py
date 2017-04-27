from django.conf.urls import url

from . import views


app_name = 'waste_schedule'
urlpatterns = [
    url(r'^details/(?P<waste_area_ids>[0-9,]*)/$', views.get_schedule_details),
    url(r'^details/(?P<waste_area_ids>[0-9,]*)/year/(?P<year>[0-9]{4})/$', views.get_schedule_details),
    url(r'^details/(?P<waste_area_ids>[0-9,]*)/year/(?P<year>[0-9]{4})/month/(?P<month>[0-9]+)/$', views.get_schedule_details),
]
