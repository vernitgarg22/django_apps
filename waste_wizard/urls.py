from django.conf.urls import url

from . import views


app_name = 'waste_wizard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^results/$', views.results, name='results'),
    url(r'^results/([ %0-9a-zA-Z]*)/$', views.ResultsView.as_view(), name='results'),
    # url(r'^results/([ %0-9a-zA-Z]*)/$', views.results, name='results'),
]
