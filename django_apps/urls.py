from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
import waste_notifier.views
import waste_schedule.views
import assessments.views
import lobbyist_data.views


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
    url(r'^waste_notifier/send/$', waste_notifier.views.send_notifications),
    url(r'^waste_notifier/confirm/$', waste_notifier.views.confirm_notifications),
    url(r'^waste_schedule/details/(?P<waste_area_ids>[0-9,]*)/$', waste_schedule.views.get_schedule_details),
    url(r'^waste_schedule/details/(?P<waste_area_ids>[0-9,]*)/year/(?P<year>[0-9]{4})/$', waste_schedule.views.get_schedule_details),
    url(r'^waste_schedule/details/(?P<waste_area_ids>[0-9,]*)/year/(?P<year>[0-9]{4})/month/(?P<month>[0-9]+)/$', waste_schedule.views.get_schedule_details),
    url(r'^assessments/address/(?P<address>[-\w\_\.\ ]+)/$', assessments.views.get_sales_property_address),
    url(r'^assessments/address/(?P<address>[-\w\_\.\ ]+)/recent/$', assessments.views.get_sales_property_address_recent),
    url(r'^assessments/address/(?P<address>[-\w\_\.\ ]+)/recent/years/(?P<years_back>[0-9]+)/$', assessments.views.get_sales_property_address),
    url(r'^assessments/(?P<pnum>[-\w\_\.]+)/$', assessments.views.get_sales_property),
    url(r'^assessments/(?P<pnum>[-\w\_\.]+)/recent/$', assessments.views.get_sales_property_recent),
    url(r'^assessments/(?P<pnum>[-\w\_\.]+)/recent/years/(?P<years_back>[0-9]+)/$', assessments.views.get_sales_property),
    
    url(r'^api/lobbyist_data$', lobbyist_data.views.lookup),
    url(r'^api/lobbyist_data/files/([0-9]*)/$', lobbyist_data.views.file),

    # waste sorter
    url(r'^waste_wizard/', include('waste_wizard.urls', namespace="waste_wizard")),
]
