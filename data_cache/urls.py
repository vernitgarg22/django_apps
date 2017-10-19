from django.conf.urls import url

from . import views


app_name = 'data_cache'
urlpatterns = [
    url(r'^(?P<name>[-\w]+)/$', views.get_data),
    url(r'^(?P<name>[-\w]+)/(?P<param>[-\w\.]+)/$', views.get_data),
]
