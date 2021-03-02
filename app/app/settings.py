"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn="https://be0b44a7b1e84ae5a21230d3cfb3b0ed@o504182.ingest.sentry.io"
        "/5590586",
    integrations=[DjangoIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tn!u@1&&t79-6aclk%0)3k%89k2u)f04^zv@dksxbnb)!e!rq-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEV_ENV' in os.environ

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'storages',
    'drf_yasg',
    'corsheaders',
    'martor',
    'core',
    'contest',
    'question',
    'submission',
    'redisboard',
    'djoser',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
}

# DJOSER = {
#     'USER_ID_FIELD' :
#     'LOGIN_FIELD' :
#     'PASSWORD_RESET_CONFIRM_URL' :
#     'USERNAME_RESET_CONFIRM_URL' :
#     'SEND_ACTIVATION_EMAIL' :
#     'SEND_CONFIRMATION_EMAIL' :
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION' :
#     'USERNAME_CHANGED_EMAIL_CONFIRMATION' :
#     'ACTIVATION_URL' :
#     'USER_CREATE_PASSWORD_RETYPE' :
#     'SET_USERNAME_RETYPE' :
#     'SET_PASSWORD_RETYPE' :
#     'PASSWORD_RESET_CONFIRM_RETYPE' :
#     'USERNAME_RESET_CONFIRM_RETYPE' :
#     'LOGOUT_ON_PASSWORD_CHANGE' :
#     'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND' :
#     'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND' :
#     'TOKEN_MODEL' :
#     'SERIALIZERS' :
#     'EMAIL' :
#     'CONSTANTS' :
#     'SOCIAL_AUTH_TOKEN_STRATEGY' :
#     'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS' :
#     'PERMISSIONS' :
#     'HIDE_USERS' :
# }

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'https://yt-list.s3.ap-south-1.amazonaws.com/staticfiles/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATICFILES_DIRS = (os.path.join('static'),)

# Allow Cross-origin resource sharing
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = ('*',)

# ADMIN PANEL

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Choices are: "semantic", "bootstrap"
MARTOR_THEME = 'semantic'

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',  # to enable/disable emoji icons.
    'imgur': 'true',  # to enable/disable imgur/custom uploader.
    'mention': 'false',  # to enable/disable mention
    'jquery': 'true',
    # to include/revoke jquery (require for admin default django)
    'living': 'false',  # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',  # to enable/disable hljs highlighting in preview
}

# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'image-upload', 'emoji',
    'direct-mention', 'toggle-maximize', 'help'
]

# To setup the martor editor with title label or not (default is False)
MARTOR_ENABLE_LABEL = False

# Imgur API Keys
MARTOR_IMGUR_CLIENT_ID = os.environ.get('MARTOR_IMGUR_CLIENT_ID')
MARTOR_IMGUR_API_KEY = os.environ.get('MARTOR_IMGUR_API_KEY')

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify'  # default
MARTOR_MARKDOWNIFY_URL = '/martor/markdownify/'  # default

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',  # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',  # to parse markdown mention
    'martor.extensions.emoji',  # to parse markdown emoji
    'martor.extensions.mdx_video',  # to parse embed/iframe video
    'martor.extensions.escape_html',  # to handle the XSS vulnerabilities
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
MARTOR_UPLOAD_URL = '/martor/uploader/'  # default
MARTOR_SEARCH_USERS_URL = '/martor/search-user/'  # default

# Markdown Extensions
# MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/'     # from webfx
MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://github.githubassets.com/images/icons/emoji/'  # default from github
MARTOR_MARKDOWN_BASE_MENTION_URL = 'https://python.web.id/author/'  # please change this to your domain

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_ADDRESSING_STYLE = "virtual"  # Required to generate signed URLs for
# getting files in Admin Panel and DRF

VERSION = '0.0.1a'

# Rest_framework Config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSIONS_CLASSES': (
        'rest_framework.permissions.isAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
        "run": "15/min",
        "run_rc": "20/min",
        "submit": "5/min",
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2)
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "YourPasswordHere1234"
        }
    }
}

CACHE_TTLS = {
    "TC": 2 * 60 * 60,
    "LANGS": 10 * 60,
    "LEADERBOARD": 1 * 60,
    "CONTEST_MAX_SCORE": 10 * 60,
    "CONTEST_QUESTIONS": 10 * 60,
    "QUESTION_DETAIL": 50 * 60,
    "RUN": 1 * 60,
    "SUBS_LIST": 5 * 60,
    "SUBMISSION": 5 * 60
}

PENALTY_MINUTES = 10
PENALTY_VERDICTS = ['WA', 'TLE', 'SIGSEGV', 'SIGXFSZ', 'SIGFPE', 'SIGABRT',
                    'RTE', 'NZEC']

MAX_RUN_OUTPUT_LENGTH = 500

# DEV ENV

if DEBUG:
    MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware', )

    INSTALLED_APPS.insert(0, 'silk')

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
    }
