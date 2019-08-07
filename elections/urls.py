from django.conf.urls import url

from . import views


app_name = 'elections'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe_notifications),
]
