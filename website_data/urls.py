from django.conf.urls import url

from . import views


app_name = 'website_data'
urlpatterns = [
    url(r'^new_content/$', views.get_new_content),
    url(r'^new_content/(?P<start>[0-9]{8})/$', views.get_new_content),
    url(r'^new_content/(?P<start>[0-9]{8})/(?P<end>[0-9]{8})/$', views.get_new_content),
    url(r'^waste_subscribers/$', views.get_subscriber_metadata),
    url(r'^waste_subscribers/(?P<start>[0-9]{8})/$', views.get_subscriber_metadata),
    url(r'^waste_subscribers/(?P<start>[0-9]{8})/(?P<end>[0-9]{8})/$', views.get_subscriber_metadata),
]
