"""Production settings and globals."""

import re
from os import environ

from corsheaders.defaults import default_headers
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

from settings.common import *


def get_env_setting(setting):
    """Get the environment setting or return exception"""
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


INSTALLED_APPS = ("corsheaders",) + INSTALLED_APPS + ("gunicorn", "storages")

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS").split(",")
########## END HOST CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get("EMAIL_HOST", "smtp.gmail.com")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD", "")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER", "your_email@example.com")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get("EMAIL_PORT", 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = "[%s] " % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting("SECRET_KEY")
########## END SECRET CONFIGURATION

# STORAGE CONFIGURATION
# settings.py


# Common settings
USE_S3 = get_env("USE_S3")
MINIO_STORAGE_ENDPOINT = get_env("MINIO_STORAGE_ENDPOINT", optional=True)
MINIO_STORAGE_ACCESS_KEY = get_env("MINIO_STORAGE_ACCESS_KEY", optional=True)
MINIO_STORAGE_SECRET_KEY = get_env("MINIO_STORAGE_SECRET_KEY", optional=True)
MINIO_STORAGE_MEDIA_BUCKET_NAME = get_env(
    "MINIO_STORAGE_MEDIA_BUCKET_NAME", optional=True
)
MINIO_STORAGE_STATIC_BUCKET_NAME = get_env(
    "MINIO_STORAGE_STATIC_BUCKET_NAME", optional=True
)
MINIO_STORAGE_USE_HTTPS = get_env("MINIO_STORAGE_USE_HTTPS", optional=True)


if USE_S3:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": MINIO_STORAGE_ACCESS_KEY,
                "secret_key": MINIO_STORAGE_SECRET_KEY,
                "bucket_name": MEDIA_URL,  # should get seperated from the ORIGINAL ONE
                "endpoint_url": f"http{'s' if MINIO_STORAGE_USE_HTTPS else ''}://{MINIO_STORAGE_ENDPOINT}",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": MINIO_STORAGE_ACCESS_KEY,
                "secret_key": MINIO_STORAGE_SECRET_KEY,
                "bucket_name": STATIC_URL,  # should get seperated from the ORIGINAL ONE
                "endpoint_url": f"http{'s' if MINIO_STORAGE_USE_HTTPS else ''}://{MINIO_STORAGE_ENDPOINT}",
            },
        },
    }


DEFAULT_FILE_STORAGE = get_env(
    "DEFAULT_FILE_STORAGE",
    default="django.core.files.storage.FileSystemStorage",
)
STATICFILES_STORAGE = get_env(
    "STATICFILES_STORAGE",
    default="django.contrib.staticfiles.storage.StaticFilesStorage",
)

# END MINIO CONFIGURATION


# CORSHEADERS CONFIGURATION
CSRF_TRUSTED_ORIGINS = get_env("CSRF_TRUSTED_ORIGINS").split(",")
CSRF_COOKIE_DOMAIN = get_env("CSRF_COOKIE_DOMAIN")
# CORS_ORIGIN_REGEX_WHITELIST = [
#     re.compile(r) for r in get_env("CORS_ORIGIN_REGEX_WHITELIST").split(",")
# ]
CORS_ALLOW_CREDENTIALS = True
# CORS_URLS_REGEX = re.compile(get_env("CORS_URLS_REGEX"))
CORS_ALLOWED_ORIGINS = list(get_env("CORS_ALLOWED_ORIGINS").split(","))
CSRF_COOKIE_SAMESITE = get_env("CSRF_COOKIE_SAMESITE")
SESSION_COOKIE_SAMESITE = get_env("SESSION_COOKIE_SAMESITE")
CSRF_COOKIE_SECURE = get_env("CSRF_COOKIE_SECURE")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

# END CORSHEADERS CONFIGURATION
DEBUG = get_env("DEBUG") == "True"

MIDDLEWARE = list(MIDDLEWARE)

# Find index of CommonMiddleware
index = MIDDLEWARE.index("django.middleware.common.CommonMiddleware")

# Insert corsheaders middleware before it
MIDDLEWARE.insert(index, "corsheaders.middleware.CorsMiddleware")


CORS_ALLOW_HEADERS = list(default_headers) + [
    "access",
]

CORS_EXPOSE_HEADERS = ["X-CSRFToken", "access"]

DEBUG = get_env("DEBUG") == "True"

# SWAGGER
ENABLE_SWAGGER = get_env("ENABLE_SWAGGER", default=False) == "True"
# END SWAGGER
