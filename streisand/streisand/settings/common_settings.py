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


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads(os.environ.get('STREISAND_DEBUG', "False").lower())
TESTING = 'test' in sys.argv

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('STREISAND_SECRET_KEY', 'you_deserve_to_be_pwned')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
]
KEY_PREFIX = 'auth_key'

MIDDLEWARE_CLASSES = ()

INSTALLED_APPS = (

    # Default apps
    'django.contrib.auth',
    'django.contrib.contenttypes',

    # Local apps
    'films',
    'film_lists',
    'invites',
    'media_formats',
    'profiles',
    'torrent_requests',
    'torrents',
    'tracker',
    'www',

    # Import scripts
    'import_scripts',
)

if DEBUG and not TESTING:
    INSTALLED_APPS += (
        'bandit',
        'django_extensions',
    )
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    BANDIT_EMAIL = os.environ.get('BANDIT_EMAIL')

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'no-reply@localhost'
DEFAULT_REPLY_TO_EMAIL = 'no-reply@localhost'

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'UTC'

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///{base_dir}/db.sqlite3".format(base_dir=BASE_DIR))

CELERY_ALWAYS_EAGER = DEBUG
CELERY_IGNORE_RESULT = True
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
BROKER_URL = REDIS_URL + '/0'
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

if TESTING:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': None,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL + '/1',
            'TIMEOUT': None,
            'KEY_PREFIX': 'auth_key',
            'KEY_FUNCTION': 'tracker.cache.make_auth_key',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

SITE_NAME = 'streisand'
SITE_URL = 'http://localhost:8000/'
TRACKER_URL = 'http://localhost:7070/'
ANNOUNCE_URL = urljoin(TRACKER_URL, '{auth_key}/announce')
