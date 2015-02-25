# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import AnnounceView

urlpatterns = patterns(
    '',
    url(r'^(?P<announce_key>[0-9a-f\-]{36})/announce/?$', AnnounceView.as_view(), name='announce'),
)
