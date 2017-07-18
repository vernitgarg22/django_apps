from django.conf.urls import url

from . import views


app_name = 'blight_tickets'
urlpatterns = [
    # url(r'^tickets/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.get_ticket_list),
    url(r'^ticket_info/(?P<parcel_id>[-\w\_\.]+)/$', views.get_ticket_info),
]
