# -*- coding: utf-8 -*-

from wiki.urls import get_pattern as get_wiki_pattern

from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.contrib.auth.views import login

from invites.views import InviteRegistrationView

from .decorators import https_required
from .views import RegistrationView, LegacyURLView, template_viewer, home


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^films/', include('films.urls')),
    url(r'^film-lists/', include('film_lists.urls')),
    url(r'^invites/', include('invites.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^torrent-requests/', include('torrent_requests.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^wiki/', get_wiki_pattern()),

    # Admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Registration
    url(r'^register/$', RegistrationView.as_view(), name='open_registration'),
    url(r'^register/(?P<invite_key>[0-9a-f\-]{36})/$', InviteRegistrationView.as_view(), name='invite_registration'),

    # Authentication
    url(r'^login/$', https_required(login), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^su/', include('django_su.urls')),

    # Utils
    url(r'^templates/(?P<template_path>.*\.html)$', template_viewer, name='template_viewer'),

    # Legacy
    url(r'^(?P<section>.+)\.php$', LegacyURLView.as_view(), name='legacy_url'),
)
