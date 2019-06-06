from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from detroitatwork import views


app_name = 'detroitatwork'
urlpatterns = [
    # url(r'^$', DetroitAtWorkFeed(), name='index'),
    url(r'^/$', views.get_rss, name='index'),
    # url(r'^$', views.DetroitAtWorkView.as_view()),
    # url(r'^$', views.IndexView.as_view(), name='index'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'rss'])
