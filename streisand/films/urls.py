# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.film_index, name='film_index'),
    url(r'^(?P<film_id>\d+)/$', views.film_details, name='film_details'),
    url(r'^(?P<film_id>\d+)/(?P<torrent_id>\d+)/$', views.film_details, name='film_torrent_details'),
]
