# -*- coding: utf-8 -*-

from .common_settings import *

INTERNAL_IPS = [
    '10.0.2.2',
]

INSTALLED_APPS += [

    # Third party apps
    'debreach',
    'django_su',
    'grappelli',

    # Default apps
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Debug Toolbar
    'debug_toolbar.apps.DebugToolbarConfig',

]

MIDDLEWARE_CLASSES += [
    'django.middleware.gzip.GZipMiddleware',
    'debreach.middleware.RandomCommentMiddleware',
    'debreach.middleware.CSRFCryptMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'www.middleware.CachedUserAuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'www.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if PRODUCTION or TESTING:
    INSTALLED_APPS.remove('debug_toolbar.apps.DebugToolbarConfig')
    MIDDLEWARE_CLASSES.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'www.urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URL_PREFIXES = (
    '/register/',
    '/logout/',
    '/__debug__/',
    '/torrents/download/',
)

OLD_SITE_HASH = os.environ.get('OLD_SITE_HASH', '')

AUTHENTICATION_BACKENDS = [
    # Case insensitive version of built-in Django authentication
    'www.auth.CaseInsensitiveAuthBackend',
    # The old site's authentication system
    'www.auth.OldSiteAuthBackend',
    # django-su
    'django_su.backends.SuBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

WSGI_APPLICATION = 'streisand.www_wsgi.application'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    # 'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'debreach.context_processors.csrf',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamped': {
            'format': '%(levelname)-8s %(asctime)-24s %(message)s'
        },
        'simple': {
            'format': '%(levelname)-8s %(message)s'
        },
    },
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
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'timestamped',
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

if TESTING:

    INSTALLED_APPS += [
        'django_nose',
    ]
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    # http://django-dynamic-fixture.readthedocs.org/en/latest/data_fixtures.html#custom-field-fixture
    DDF_FIELD_FIXTURES = {
        'picklefield.fields.PickledObjectField': {
            'ddf_fixture': lambda: [],
        },
    }
    DDF_FILL_NULLABLE_FIELDS = False

    # Make the tests faster by using a fast, insecure hashing algorithm
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': None,
        }
    }
