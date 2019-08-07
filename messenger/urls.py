from django.conf.urls import url

from messenger import views


app_name = 'messenger'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe),
]
