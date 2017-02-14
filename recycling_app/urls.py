"""recycling_app URL Configuration

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


urlpatterns = [
	# url(r'^$', RedirectView.as_view(url='waste_wizard/', permanent=False), name='index'),
	url(r'^$', RedirectView.as_view(url='http://app.detroitmi.gov/codcityservices/', permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^waste_wizard/', include('waste_wizard.urls', namespace="waste_wizard")),
]
