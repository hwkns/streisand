# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import TorrentUploadView, TorrentDownloadView


urlpatterns = patterns(
    'torrents.views',
    url(r'^$', 'torrent_index', name='torrent_index'),
    url(r'^(?P<torrent_id>\d+)/$', 'torrent_details', name='torrent_details'),
    url(r'^upload/$', TorrentUploadView.as_view(), name='torrent_upload'),
    url(
        r'^download/(?P<torrent_id>\d+)/(?P<announce_key>[0-9a-f\-]{36})/?$',
        TorrentDownloadView.as_view(),
        name='torrent_download'
    ),
)
