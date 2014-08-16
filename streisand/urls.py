# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
# from django.contrib import admin

from streisand.tracker.views import AnnounceView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<auth_key>.{16})/announce/?$',
        AnnounceView.as_view(), name='announce'
    ),
    # url(r'^admin/', include(admin.site.urls)),
)
