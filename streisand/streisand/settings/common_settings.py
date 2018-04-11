# -*- coding: utf-8 -*-
"""
Django settings for streisand project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import sys
import json
from urllib.parse import urljoin

import dj_database_url

from django.utils.timezone import timedelta

AUTH_USER_MODEL = 'users.User'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads(os.environ.get('STREISAND_DEBUG', "False").lower())
PRODUCTION = not DEBUG
TESTING = 'test' in sys.argv
TEST_RUNNER = 'streisand.test_utils.CustomTestSuiteRunner'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('STREISAND_SECRET_KEY', 'you_deserve_to_be_pwned')


ALLOWED_HOSTS = [
    # Adding this for development
    'localhost',
    '.jumpcut.to',
]

if DEBUG:
    ALLOWED_HOSTS = ['*']


HOST_DOMAIN = os.environ.get('HOST_DOMAIN', '')
if HOST_DOMAIN:
    ALLOWED_HOSTS.append('.' + HOST_DOMAIN)

INSTALLED_APPS = [

    # Default apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'www.apps.SuitConfig',

    # Local apps
    'comments',
    'films',
    'forums',
    'imdb',
    'invites',
    'media_formats',
    'mediainfo',
    'rotten_tomatoes',
    'tests',
    'torrent_requests',
    'torrent_stats',
    'torrents',
    'tracker',
    'users',
    'wiki',
    'www',

]

if DEBUG and not TESTING:
    INSTALLED_APPS += [
        'bandit',
        'django_extensions',
    ]
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    BANDIT_EMAIL = os.environ.get('BANDIT_EMAIL')

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'streisand.tracker@gmail.com'
DEFAULT_REPLY_TO_EMAIL = 'streisand.tracker@gmail.com'

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'UTC'

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///{base_dir}/db.sqlite3'.format(base_dir=BASE_DIR))

CELERY_ALWAYS_EAGER = DEBUG
CELERY_IGNORE_RESULT = True
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
BROKER_URL = REDIS_URL + '/0'
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL + '/1',
        'TIMEOUT': None,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

if PRODUCTION:
    DATABASES['default']['CONN_MAX_AGE'] = None

SITE_NAME = 'Streisand'
SITE_URL = 'http://localhost:8000/'
TRACKER_URL = 'http://localhost:7070/'
TRACKER_ANNOUNCE_INTERVAL = timedelta(minutes=40)
TRACKER_ANNOUNCE_URL_TEMPLATE = urljoin(TRACKER_URL, '{announce_key}/announce')
