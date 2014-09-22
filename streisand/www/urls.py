# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^$', 'www.views.home', name='home'),
    url(r'^films/', include('films.urls')),
    url(r'^film-lists/', include('film_lists.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
