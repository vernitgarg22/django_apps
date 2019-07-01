from django.conf.urls import url

from . import views


app_name = 'car_info'
urlpatterns = [
    url(r'^$', views.add_polling_location),
]
