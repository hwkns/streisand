# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^$', 'www.views.home', name='home'),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
