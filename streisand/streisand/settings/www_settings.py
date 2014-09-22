# -*- coding: utf-8 -*-

from .common_settings import *

INSTALLED_APPS += (

    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'www',
    'films',
    'film_lists',
    'profiles',
    'torrents',
    'tracker',

)

MIDDLEWARE_CLASSES += (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'www.urls'

WSGI_APPLICATION = 'streisand.www_wsgi.application'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # 'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'streisand': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

if DEBUG:
    INSTALLED_APPS += (
        'django_nose',
    )
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


# http://django-dynamic-fixture.readthedocs.org/en/latest/data_fixtures.html#custom-field-fixture
DDF_FIELD_FIXTURES = {
    'picklefield.fields.PickledObjectField': {
        'ddf_fixture': lambda: [],
    },
}
