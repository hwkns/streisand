# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.shortcuts import redirect

from .views import TorrentUploadView, TorrentDownloadView, TorrentModerationView, new_reseed_request, reseed_request_index


urlpatterns = patterns(
    'torrents.views',
    url(r'^$', lambda r: redirect('film_index')),
    url(
        regex=r'^upload/?$',
        view=TorrentUploadView.as_view(),
        name='torrent_upload',
    ),
    url(
        regex=r'^(?P<torrent_id>\d+)/download/(?P<announce_key>[0-9a-f\-]{36})/?$',
        view=TorrentDownloadView.as_view(),
        name='torrent_download',
    ),
    url(
        regex=r'^(?P<torrent_id>\d+)/moderate/?$',
        view=TorrentModerationView.as_view(),
        name='torrent_moderation',
    ),
    url(
        regex=r'^(?P<torrent_id>\d+)/request-reseed/?$',
        view=new_reseed_request,
        name='reseed_request',
    ),
    url(
        regex=r'^reseed-requests/?$',
        view=reseed_request_index,
        name='reseed_request_index',
    ),
)
