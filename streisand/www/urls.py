# -*- coding: utf-8 -*-

import debug_toolbar

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import request

from invites.views import InviteRegistrationView
from .decorators import https_required
from .views import RegistrationView, LegacyURLView, template_viewer, home, login

swagger_info = openapi.Info(
      title="JumpCut.to API",
      default_version='v1',
      description="JumpCut API",
      terms_of_service="https://www.jumpcut.to/terms/",
      contact=openapi.Contact(email="admin@jumpcut.to"),
   )

SchemaView = get_schema_view(
      validators=['ssv', 'flex'],
      public=False,
      permission_classes=(permissions.IsAdminUser,),
)

@api_view(['GET'])
def plain_view(request):
    pass




urlpatterns = [

    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


    # Not sure if we need this yet
    url(r'^redoc/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    url(
        regex=r'^$',
        view=home,
        name='home'
    ),
    url(r'^films/', include('films.urls')),
    url(r'^film-lists/', include('film_lists.urls')),
    url(r'^forums/', include('forums.urls')),
    url(r'^invites/', include('invites.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^torrent-requests/', include('torrent_requests.urls')),
    url(r'^torrent-stats/', include('torrent_stats.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^wiki/', include('wiki.urls')),

    # Admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    # Registration
    url(
        regex=r'^register/$',
        view=RegistrationView.as_view(),
        name='open_registration',
    ),
    url(
        regex=r'^register/(?P<invite_key>[0-9a-f\-]{36})/$',
        view=InviteRegistrationView.as_view(),
        name='invite_registration',
    ),

    # Authentication
    url(
        regex=r'^login/$',
        view=https_required(login),
        name='login',
    ),
    url(
        regex=r'^logout/$',
        view=logout_then_login,
        name='logout',
    ),
    url(r'^su/', include('django_su.urls')),

    # Utils
    url(
        regex=r'^templates/(?P<template_path>.*\.html)$',
        view=template_viewer,
        name='template_viewer',
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
