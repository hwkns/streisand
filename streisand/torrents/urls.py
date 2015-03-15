# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.shortcuts import redirect

from .views import TorrentUploadView, TorrentDownloadView


urlpatterns = patterns(
    'torrents.views',
    url(r'^$', lambda r: redirect('film_index')),
    url(r'^upload/$', TorrentUploadView.as_view(), name='torrent_upload'),
    url(
        r'^(?P<torrent_id>\d+)/download/(?P<announce_key>[0-9a-f\-]{36})/?$',
        TorrentDownloadView.as_view(),
        name='torrent_download'
    ),
)
