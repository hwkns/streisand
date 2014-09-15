# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
# from django.contrib import admin


urlpatterns = patterns(
    'www.views',
    url(r'^$', 'home', name='home'),
    # url(r'^admin/', include(admin.site.urls)),
)
