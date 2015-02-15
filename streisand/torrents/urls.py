# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import TorrentUploadView


urlpatterns = patterns(
    'torrents.views',
    url(r'^$', 'torrent_index', name='torrent_index'),
    url(r'^(?P<torrent_id>\d+)/$', 'torrent_details', name='torrent_details'),
    url(r'^upload/$', TorrentUploadView.as_view(), name='torrent_upload'),
    url(r'^download/(?P<torrent_id>\d+)/$', 'torrent_download', name='torrent_download'),
)
