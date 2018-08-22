from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
import assessments.views
import blight_tickets.views
import data_cache.views
import elections.views
import photo_survey.views
import property_data.views
import waste_notifier.views
import waste_schedule.views
import website_data.views



# To change this see 
# http://stackoverflow.com/questions/4938491/django-admin-change-header-django-administration-text
admin.site.site_header = 'System Admin'


urlpatterns = [

    # root redirects to waste_wizard
	url(r'^$', RedirectView.as_view(url='waste_wizard/', permanent=False), name='index'),

    # admin site
    url(r'^admin/', admin.site.urls),
    url(r'^admin/waste_schedule/', include('waste_schedule.urls', namespace='waste_schedule')),

    # apis
    url(r'^assessments/', include('assessments.urls', namespace="assessments")),
    url(r'^blight_tickets/', include('blight_tickets.urls', namespace="blight_tickets")),
    url(r'^data_cache/', include('data_cache.urls', namespace="data_cache")),
    url(r'^elections/', include('elections.urls', namespace="elections")),
    url(r'^photo_survey/', include('photo_survey.urls', namespace="photo_survey")),
    url(r'^property_data/', include('property_data.urls', namespace="property_data")),
    url(r'^waste_notifier/', include('waste_notifier.urls', namespace="waste_notifier")),
    url(r'^waste_schedule/', include('waste_schedule.urls', namespace="waste_schedule")),
    url(r'^weather_info/', include('weather_info.urls', namespace="weather_info")),
    url(r'^website_data/', include('website_data.urls', namespace="website_data")),
    
    # waste sorter
    url(r'^waste_wizard/', include('waste_wizard.urls', namespace="waste_wizard")),
]
