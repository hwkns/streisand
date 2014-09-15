# -*- coding: utf-8 -*-

from .common_settings import *

INSTALLED_APPS += (
    'tracker',
)

ROOT_URLCONF = 'tracker.urls'

WSGI_APPLICATION = 'streisand.tracker_wsgi.application'
