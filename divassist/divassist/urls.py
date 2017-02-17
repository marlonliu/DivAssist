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
]