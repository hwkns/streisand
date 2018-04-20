# -*- coding: utf-8 -*-

import debug_toolbar

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from .views import LegacyURLView, template_viewer, home
from django.http import HttpResponseRedirect


urlpatterns = [
    # Redirect to API
    url(r'^home', lambda r: HttpResponseRedirect('/')),

    # API
    url(r'^api/v1/', include('interfaces.api_site.urls')),

    # API Core-Schema Docs TODO: Update this when better Api Docs come out and work.
    url(r'^docs/', include_docs_urls(title='JumpCut API v1', public=False)),

    # Docs that need updating. Made with Sphinx
    url(r'^model-docs/', include('docs.urls')),

    # URLS that gotta go.
    url(r'^films/', include('films.urls')),
    url(r'^forums/', include('forums.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^torrent-requests/', include('torrent_requests.urls')),
    url(r'^torrent-stats/', include('torrent_stats.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^wiki/', include('wiki.urls')),

    # Admin
    url(r'^admin/', admin.site.urls),
    url(r'^admin/docs/', include('django.contrib.admindocs.urls')),


    # Authentication
    url(r'^su/', include('django_su.urls')),

    # Utils
    url(
        regex=r'^templates/(?P<template_path>.*\.html)$',
        view=template_viewer,
        name='template_viewer',
    ),

    url(
        regex=r'^$',
        view=home,
        name='home',
    ),

    # Legacy
    url(
        regex=r'^(?P<section>.+)\.php$',
        view=LegacyURLView.as_view(),
        name='legacy_url',
    ),
]

if settings.DEBUG:
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
