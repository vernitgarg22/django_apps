from django.conf.urls import url

from . import views


# TODO get workaround for django's handling of '.' - override lookup_value_regex in router
# https://docs.djangoproject.com/en/1.11/topics/http/urls/
# https://stackoverflow.com/questions/41580450/url-with-dot-in-django-rest-framework
# https://github.com/encode/django-rest-framework/issues/2248
# https://stackoverflow.com/questions/27963899/django-rest-framework-using-dot-in-url


app_name = 'photo_survey'
urlpatterns = [

    url(r'^auth_token/$', views.get_auth_token),

    url(r'^count/(?P<parcel_id>[-\w\_\.]+)/$', views.get_survey_count),
    url(r'^status/$', views.get_status),
    url(r'^(?P<parcel_id>[-\w\_\.]+)/$', views.get_metadata),
    # url(r'^(?P<parcel_id>[-\w\_\.]+)/$', views.get_metadata, lookup_value_regex = '[^/]+'),
    url(r'^survey/(?P<parcel_id>[-\w\_\.]+)/$', views.post_survey),
    url(r'^surveyor/survey_count/$', views.get_surveyor_survey_count),
]
