from django.conf.urls import include, url
from divassist_web.views import *

from django.contrib.auth import views as auth_views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', login_page),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register),
    url(r'^home_page/$', home_page),
    url(r'^registration/select_home_station/$', select_home_station),
    url(r'^registration/change_password/$', change_password),
    # url(r'^rides/add_ride/$', add_ride),
    # url(r'^rides/ride_created/$', ride_created),
    # url(r'^rides/search_rides/$', search_ride),
    # url(r'^rides/view_ride/$', view_ride),
    url(r'^upload_ride/$', add_ride),
    url(r'^rides/ride_created/$', ride_created),
    url(r'^search_ride/$', search_ride),
    url(r'^view_rides/$', view_all_rides),
    url(r'^no_matching_rides/$', no_matching_rides),
    url(r'^landing/(?P<time>[0-9]+)/$', landing),
    url(r'^prediction/(?P<day>[0-9]+)/(?P<hour>[0-9]+)/.*$', prediction)
]