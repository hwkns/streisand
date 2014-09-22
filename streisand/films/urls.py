# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'films.views',
    url(r'^/?$', 'film_index', name='film_index'),
    url(r'^(?P<film_id>\d+)/?$', 'film_details', name='film_details'),
)
