"""
Django settings for hotel_hp project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import datetime as dt
from dotenv import load_dotenv
from celery.schedules import crontab

# Load .env variables.
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
]

if value := os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS += value.split(',')

CSRF_TRUSTED_ORIGINS = [
]

if value := os.environ.get('ALLOWED_ORIGINS'):
    ALLOWED_HOSTS += value.split(',')

# Application definition

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps (installed from pip)
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'celery',
    'drf_spectacular',
    'drf_yasg',
    'graphene_django',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # Local apps (user-defined)
    'hotel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'hotel_hp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hotel_hp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_MYSQL = {
    'ENGINE': 'django.db.backends.mysql',
    'OPTIONS': {
        'read_default_file': str(BASE_DIR / 'my.cnf'),
    },
    'NAME': os.environ.get('DB_NAME'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': '3306',
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
}

DB_PSQL = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('DB_NAME'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': '5432',
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
}

DB_SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

DATABASES = {
    # Use MySQL as a default.
    'default': DB_MYSQL,
}

DB_TYPE = os.environ.get('DB_TYPE')

if DB_TYPE == 'PSQL':
    DATABASES['default'] = DB_PSQL
elif DB_TYPE == 'SQLite':
    DATABASES['default'] = DB_SQLITE

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')

if RABBITMQ_HOST is not None:
    CELERY_BROKER_URL = f'amqp://{RABBITMQ_HOST}:5672/'
else:
    REDIS_HOST = os.environ.get('REDIS_HOST')
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:6379/0'


CELERY_BEAT_SCHEDULE = {
    'cleanup_shifts': {
        'task': 'hotel.tasks.cleanup_shifts',
        'schedule': crontab(minute='0', hour='1'),
    },
    'populate_shifts': {
        'task': 'hotel.tasks.populate_shifts',
        'schedule': crontab(minute='0', hour='1'),
    },
    'cleanup_old_reservations': {
        'task': 'hotel.tasks.cleanup_old_reservations',
        'schedule': crontab(minute='0', hour='1'),
    },
    'cleanup_unpaid_reservations': {
        'task': 'hotel.tasks.cleanup_unpaid_reservations',
        'schedule': dt.timedelta(minutes=15),
    },
    'reservation_daily_stats': {
        'task': 'products.tasks.reservation_daily_stats',
        'schedule': crontab(minute='0', hour='8'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True

GRAPHENE = {
    'SCHEMA': 'hotel_hp.schema.schema'
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
    },
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

WSGI_APPLICATION = "hotel_hp.wsgi.application"
