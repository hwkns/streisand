# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.contrib.auth.views import login

from .decorators import https_required
from .views import RegistrationView


urlpatterns = patterns(
    '',
    url(r'^$', 'www.views.home', name='home'),
    url(r'^films/', include('films.urls')),
    url(r'^film-lists/', include('film_lists.urls')),
    url(r'^profile/', include('profiles.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^register/$', RegistrationView.as_view(), name='open_registration'),
    url(r'^register/(?P<invite_key>[0-9a-f\-]{36})/$', RegistrationView.as_view(), name='invite_registration'),
    url(r'^login/$', https_required(login), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^su/', include('django_su.urls')),
)
