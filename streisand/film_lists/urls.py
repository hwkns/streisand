# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'film_lists.views',
    url(r'^/?$', 'film_list_index', name='film_list_index'),
    url(r'^(?P<film_list_id>\d+)/?$', 'film_list_details', name='film_list_details'),
)
