from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
import assessments.views
import waste_notifier.views
import waste_schedule.views



# To change this see 
# http://stackoverflow.com/questions/4938491/django-admin-change-header-django-administration-text
admin.site.site_header = 'Waste Admin'


urlpatterns = [

    # root redirects to waste_wizard
	url(r'^$', RedirectView.as_view(url='waste_wizard/', permanent=False), name='index'),

    # admin site
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/waste_schedule/', include('waste_schedule.urls', namespace='waste_schedule')),

    # apis
    url(r'^waste_notifier/', include('waste_notifier.urls', namespace="waste_notifier")),
    url(r'^waste_schedule/', include('waste_schedule.urls', namespace="waste_schedule")),
    url(r'^assessments/address/(?P<address>[-\w\_\.\ ]+)/$', assessments.views.get_sales_property_address),
    url(r'^assessments/address/(?P<address>[-\w\_\.\ ]+)/recent/$', assessments.views.get_sales_property_address_recent),
    url(r'^assessments/address/(?P<address>[-\w\_\.\ ]+)/recent/years/(?P<years_back>[0-9]+)/$', assessments.views.get_sales_property_address),
    url(r'^assessments/(?P<pnum>[-\w\_\.]+)/$', assessments.views.get_sales_property),
    url(r'^assessments/(?P<pnum>[-\w\_\.]+)/recent/$', assessments.views.get_sales_property_recent),
    url(r'^assessments/(?P<pnum>[-\w\_\.]+)/recent/years/(?P<years_back>[0-9]+)/$', assessments.views.get_sales_property),
    url(r'^weather_info/', include('weather_info.urls', namespace="weather_info")),
    
    # waste sorter
    url(r'^waste_wizard/', include('waste_wizard.urls', namespace="waste_wizard")),
]
