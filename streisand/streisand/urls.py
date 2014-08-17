# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
# from django.contrib import admin

from tracker.views import AnnounceView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<auth_key>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/announce/?$',
        AnnounceView.as_view(), name='announce'
    ),
    # url(r'^admin/', include(admin.site.urls)),
)
