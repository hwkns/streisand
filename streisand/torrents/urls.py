# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'torrents.views',
    url(r'^/?$', 'index', name='torrent_index'),
    url(r'^(?P<torrent_id>\d+)/?$', 'torrent_view', name='torrent'),
)
