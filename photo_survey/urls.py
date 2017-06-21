from django.conf.urls import url

from . import views


app_name = 'photo_survey'
urlpatterns = [
    url(r'^count/(?P<parcel_id>[-\w\_\.]+)/$', views.get_survey_count),
    url(r'^(?P<parcel_id>[-\w\_\.]+)/$', views.get_metadata),
    url(r'^image/(?P<image_id>[-\w\_\.]+)/$', views.get_image),
]
