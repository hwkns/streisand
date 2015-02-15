# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'torrent_requests.views',
    url(r'^$', 'torrent_request_index', name='torrent_request_index'),
    url(r'^(?P<torrent_request_id>\d+)/$', 'torrent_request_details', name='torrent_request_details'),
)
