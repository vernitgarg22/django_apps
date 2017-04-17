from django.conf.urls import url

from . import views


app_name = 'report_dumping'
urlpatterns = [
    url(r'^$', views.report),
    url(r'list_services/$', views.list_services),
]
