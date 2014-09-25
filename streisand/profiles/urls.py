# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'profiles.views',
    url(r'^/?$', 'user_profile_redirect', name='user_profile_redirect'),
    url(r'^(?P<profile_id>\d+)/?$', 'user_profile', name='user_profile'),
)
