from django.conf.urls import url

from . import views


app_name = 'data_cache'
urlpatterns = [

    url(r'^data/$', views.add_data),
    url(r'^url_cache/urls/$', views.add_url),
    url(r'^city_data_summaries/$', views.get_city_data_summaries),
    url(r'^refresh/$', views.refresh_cache),
    url(r'^(?P<name>[-\w]+)/$', views.get_data, name="data-set"),
    url(r'^(?P<name>[-\w]+)/(?P<param>[-\w\.]+)/$', views.get_data),
]
