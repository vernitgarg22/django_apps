from django.conf.urls import url

from . import views


app_name = 'data_cache'
urlpatterns = [
    url(r'^(?P<name>[-\w]+)/$', views.get_data),
]
