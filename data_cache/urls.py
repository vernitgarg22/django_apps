from django.conf.urls import url

from . import views


app_name = 'data_cache'
urlpatterns = [

    # TODO clean this up
    # url(r'^url_cache/(?P<url>[-\w\.\%]+)/$', views.get_url),
    url(r'^url_cache/.*/$', views.get_url),
    url(r'^(?P<name>[-\w]+)/$', views.get_data),
    url(r'^(?P<name>[-\w]+)/(?P<param>[-\w\.]+)/$', views.get_data),
]
