# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import torrent_request_index, TorrentRequestView, NewTorrentRequestView


urlpatterns = patterns(
    'torrent_requests.views',
    url(
        regex=r'^$',
        view=torrent_request_index,
        name='torrent_request_index',
    ),
    url(
        regex=r'^(?P<torrent_request_id>\d+)/$',
        view=TorrentRequestView.as_view(),
        name='torrent_request_details',
    ),
    url(
        regex=r'^new/$',
        view=NewTorrentRequestView.as_view(),
        name='new_torrent_request',
    )
)
