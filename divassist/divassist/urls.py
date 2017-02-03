from django.conf.urls import patterns, include, url
from divassist_web.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^home_page/$', home_page),
    url(r'^registration/select_home_station/$', select_home_station),
)