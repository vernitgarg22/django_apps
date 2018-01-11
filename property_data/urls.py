from django.conf.urls import url

from . import views


app_name = 'property_data'
urlpatterns = [

    url(r'^dte/active_connections/(?P<parcel_id>[-\w\_\.\ ]+)/$', views.get_dte_active_connection),
]
