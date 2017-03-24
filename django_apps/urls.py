from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
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
    url(r'^api/waste_schedule/changes/([0-9]*)/$', waste_schedule.views.get_schedule_changes),
    url(r'^waste_schedule/details/([0-9]*)/$', waste_schedule.views.get_schedule_details),
    # url(r'^assessments/([a-zA-Z0-9\.\-]*)/$', assessments.views.get_sales_property),
    url(r'^assessments/(?P<pnum>[-\w\.]+)/$', assessments.views.get_sales_property),
    
    url(r'^api/lobbyist_data$', lobbyist_data.views.lookup),
    url(r'^api/lobbyist_data/files/([0-9]*)/$', lobbyist_data.views.file),

    # waste sorter
    url(r'^waste_wizard/', include('waste_wizard.urls', namespace="waste_wizard")),
]
