import os
from urllib.parse import urlparse

import launchflow as lf
from django_backend.infra import ecs_fargate, postgres, redis, storage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TODO(developer): Update the secret key before deploying to production!
SECRET_KEY = "your_secret_key"

# This utility function returns True if the application is running on Cloud Run
if lf.is_deployment():
    # Fetches the service URL from the Cloud Run Service
    service_url = ecs_fargate.outputs().service_url

    DEBUG = False
    ALLOWED_HOSTS = [urlparse(service_url).netloc]
    CSRF_TRUSTED_ORIGINS = [service_url]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

else:
    DEBUG = True
    ALLOWED_HOSTS = ["*"]

# Fetches the Django options for the Postgres instance hosted on Cloud SQL
DATABASES = {"default": postgres.django_settings()}

# Fetches the Django options for the Redis instance hosted on Memorystore
CACHES = {"default": redis.django_settings()}

STORAGES = {
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
    }
}
STATIC_URL = "/static/"

# Fetches the information for the S3 bucket and populates the django-storages settings
AWS_STORAGE_BUCKET_NAME = storage.outputs().bucket_name


# The rest of the settings below are boilerplate Django settings
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ROOT_URLCONF = "django_backend.urls"

WSGI_APPLICATION = "django_backend.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
