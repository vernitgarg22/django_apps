from django.conf.urls import url

from . import views


app_name = 'waste_wizard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^items/$', views.ItemsView.as_view(), name='items'),
    url(r'^results/$', views.ResultsView.as_view(), name='results'),
    url(r'^results/([ %0-9a-zA-Z\,]*)/$', views.ResultsView.as_view(), name='results'),
    url(r'^detail/([ %0-9a-zA-Z\,]*)/$', views.DetailView.as_view(), name='detail'),
]
