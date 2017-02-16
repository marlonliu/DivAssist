from django.conf.urls import include, url
from divassist_web.views import *

from django.contrib.auth import views as auth_views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', auth_views.login),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', auth_views.login), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^home_page/$', home_page),
    url(r'^registration/select_home_station/$', select_home_station),
]