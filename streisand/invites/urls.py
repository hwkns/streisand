# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import InviteView


urlpatterns = patterns(
    'invites.views',
    url(r'^$', InviteView.as_view(), name='invite_index'),
)
