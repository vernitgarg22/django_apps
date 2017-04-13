from django.conf.urls import url

from . import views


app_name = 'weather_info'
urlpatterns = [
    url(r'^latest/$', views.get_latest),
]
