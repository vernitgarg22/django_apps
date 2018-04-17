from django.conf.urls import url

from . import views


app_name = 'assessments'
urlpatterns = [
    url(r'^address/(?P<address>[-\w\_\.\ ]+)/$', views.get_sales_property_address),
    url(r'^address/(?P<address>[-\w\_\.\ ]+)/recent/$', views.get_sales_property_address_recent),
    url(r'^address/(?P<address>[-\w\_\.\ ]+)/recent/years/(?P<years_back>[0-9]+)/$', views.get_sales_property_address),

    # url(r'^(?P<pnum>[\.\w-]+)/$', views.get_sales_property),
    # url(r'^(?P<pnum>[-\w]+)/$', views.get_sales_property),
    url(r'^(?P<pnum>[-\w\_\.]+)/$', views.get_sales_property),
    url(r'^(?P<pnum>[-\w\_\.]+)/recent/$', views.get_sales_property_recent),
    url(r'^(?P<pnum>[-\w\_\.]+)/recent/years/(?P<years_back>[0-9]+)/$', views.get_sales_property),

    url(r'^(?P<pnum>[-\w\_\.]+)/images/$', views.get_images),

    # url(r'^parcel/owner_groups/$', views.get_parcel_ownership_groups),
    url(r'^parcel/owner_groups/$', views.ParcelOwnershipGroupsView.as_view(), name='owner_groups'),
    url(r'^parcel/(?P<pnum>[-\w\_\.]+)/$', views.get_parcel),

    url(r'rentals/cases/(?P<pnum>[-\w\_\.\ ]+)/$', views.get_rental_cases),
]
