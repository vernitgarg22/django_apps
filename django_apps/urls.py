"""django_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
import waste_schedule.views
import lobbyist_data.views


# To change this see 
# http://stackoverflow.com/questions/4938491/django-admin-change-header-django-administration-text
admin.site.site_header = 'Waste Admin'


urlpatterns = [
	url(r'^$', RedirectView.as_view(url='waste_wizard/', permanent=False), name='index'),
    url(r'^api/waste_schedule/changes/([0-9]*)/$', waste_schedule.views.get_schedule_changes),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/waste_schedule/', include('waste_schedule.urls', namespace='waste_schedule')),
    url(r'^waste_wizard/', include('waste_wizard.urls', namespace="waste_wizard")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/lobbyist_data$', lobbyist_data.views.lookup),
    url(r'^api/lobbyist_data/files/([0-9]*)/$', lobbyist_data.views.file),
]
