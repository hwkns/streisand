# -*- coding: utf-8 -*-

from .common_settings import *

INTERNAL_IPS = [
    '10.0.2.2',
]

INSTALLED_APPS += [

    # Third party apps
    'django_su',
    'grappelli',

    # Contrib apps
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # Debug Toolbar
    'debug_toolbar',

    # Import scripts
    'import_scripts',

]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'www.middleware.CachedUserAuthenticationMiddleware',
    'www.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'profiles.middleware.IPHistoryMiddleware',
]

if PRODUCTION or TESTING:
    INSTALLED_APPS.remove('debug_toolbar')
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'www.urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URL_PREFIXES = (
    '/__debug__/',
    '/register/',
    '/logout/',
    '/torrents/download/',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'www.auth.OldSitePasswordHasher',
]

RT_API_KEY = os.environ.get('RT_API_KEY', '')
OLD_SITE_SECRET_KEY = os.environ.get('OLD_SITE_HASH', '')

AUTHENTICATION_BACKENDS = [
    # Case insensitive authentication, custom permissions
    'www.auth.CustomAuthBackend',
    # django-su
    'django_su.backends.SuBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

WSGI_APPLICATION = 'streisand.www_wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
]

ITEMS_PER_PAGE = 50


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
