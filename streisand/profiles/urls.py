# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'profiles.views',
    url(r'^/?$', 'index', name='profile_index'),
    url(r'^(?P<profile_id>\d+)/?$', 'profile_view', name='user_profile'),
)
