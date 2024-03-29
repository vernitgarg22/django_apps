from django.conf.urls import url

from . import views


app_name = 'photo_survey'
urlpatterns = [

    url(r'^auth_token/$', views.get_auth_token),

    url(r'^count/(?P<parcel_id>[-\w\_\.]+)/$', views.get_survey_count),
    url(r'^status/$', views.get_status),
    url(r'^status/summary/$', views.get_status_summary),
    url(r'^(?P<parcel_id>[-\w\_\.]+)/$', views.get_metadata),
    url(r'^survey/(?P<parcel_id>[-\w\_\.]+)/$', views.SurveyorView.as_view(), name='survey'),
    url(r'^survey/data/(?P<survey_id>[0-9]+)/$', views.get_survey),
    url(r'^survey/latest/(?P<parcel_id>[-\w\_\.]+)/$', views.get_latest_survey),
    url(r'^surveyor/survey_count/$', views.get_surveyor_survey_count),

    # endpoints specific to bridging neighborhoods
    url(r'^bridging_neighborhoods/favorites/(?P<parcel_id>[-\w\_\.]+)/$', views.BridgingNeighborhoodsView.as_view(), name='bridging_neighborhoods'),
    url(r'^bridging_neighborhoods/(?P<username>[-\w\_\.]+)/favorites/$', views.BridgingNeighborhoodsView.as_view(), name='bridging_neighborhoods'),
    url(r'^bridging_neighborhoods/(?P<username>[-\w\_\.]+)/favorites/(?P<parcel_id>[-\w\_\.]+)/$', views.BridgingNeighborhoodsView.as_view(), name='bridging_neighborhoods'),
]
