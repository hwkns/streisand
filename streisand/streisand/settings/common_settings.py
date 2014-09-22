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


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4$91je#^q%*m*!g^y^webtfaw0k3(c4vz^9%w0^i4)l=inf&-#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads(os.environ.get('STREISAND_DEBUG', "False").lower())
TESTING = 'test' in sys.argv

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
KEY_PREFIX = 'auth_key'

# Application definition

INSTALLED_APPS = ()

if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
    )

MIDDLEWARE_CLASSES = ()


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': None,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '127.0.0.1:6379:1',
            'TIMEOUT': None,
            'KEY_PREFIX': 'auth_key',
            'KEY_FUNCTION': 'tracker.cache.make_auth_key',
            'OPTIONS': {
                'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            }
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

CELERY_ALWAYS_EAGER = TESTING
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
