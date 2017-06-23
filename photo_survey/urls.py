from django.conf.urls import url

from . import views


app_name = 'photo_survey'
urlpatterns = [
    url(r'^count/(?P<parcel_id>[-\w\_\.]+)/$', views.get_survey_count),
    url(r'^(?P<parcel_id>[-\w\_\.]+)/$', views.get_metadata),
    # url(r'^(?P<parcel_id>[-\w\_\.]+)/$', views.get_metadata, lookup_value_regex = '[^/]+'),
    url(r'^image/(?P<image_path>.+)/$', views.get_image),
    url(r'^survey/(?P<parcel_id>[-\w\_\.]+)/$', views.post_survey),
]
