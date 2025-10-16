"""Common settings"""

from os.path import abspath, dirname
from pathlib import Path
from sys import path

from dotenv import load_dotenv

from settings.utils import get_env

# * PATH CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent.parent

# Absolute filesystem path to the project directory:
PROJECT_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level package folder:
PACKAGE_ROOT = dirname(PROJECT_ROOT)

# .env file path
env_path = Path(PROJECT_ROOT) / ".env"

# .ENV CONFIGURATION
load_dotenv(dotenv_path=env_path)
# END .ENV CONFIGURATION

# Site name:
SITE_NAME = get_env("SITE_NAME")
SITE_ID = get_env("SITE_ID")

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(PACKAGE_ROOT)
# * END PATH CONFIGURATION

# * DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = get_env("DEBUG") == "True"

# * DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env("DEFAULT_DATABASE_NAME"),
        "USER": get_env("DEFAULT_DATABASE_USER"),
        "PASSWORD": get_env("DEFAULT_DATABASE_PASSWORD"),
        "HOST": get_env("DEFAULT_DATABASE_HOST"),
        "PORT": get_env("DEFAULT_DATABASE_PORT"),
        "TEST": {
            "DEPENDENCIES": [],
        },
        "OPTIONS": {
            "pool": {
                "min_size": 2,
                "max_size": 4,
                "timeout": 10,
            }
        },
    },
}
# DATABASE_ROUTERS = ("src.core.dbrouter.DatabaseAppsRouter",)
# * END DATABASE CONFIGURATION

# * PASSWORD CONFIGURATION
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# * END PASSWORD CONFIGURATION

# * GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = "UTC"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = get_env("LANGUAGE_CODE")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# * END GENERAL CONFIGURATION

# * MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = get_env("MEDIA_ROOT")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = get_env("MEDIA_URL")
# * END MEDIA CONFIGURATION

# * STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = get_env("STATIC_ROOT")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = get_env("STATIC_URL")
# * END STATIC FILE CONFIGURATION

# * SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = "django-insecure-!p(60+v&)rpxev((#rj()ltf!mre0i8kb5&3+u8h*20pisvayz"
# * END SECRET CONFIGURATION

# *SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", default="localhost").split(",")
DEFAULT_DOMAIN = get_env("DEFAULT_DOMAIN")
# * END SITE CONFIGURATION

# * TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / get_env("TEMPLATE_DIR"),
        ],
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
# * END TEMPLATE CONFIGURATION

# * MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# * END MIDDLEWARE CONFIGURATION

# * URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "src.core.urls"
# * END URL CONFIGURATION


# * APP CONFIGURATION
DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src.api",
    "src.apps.authentication",
    "src.apps.profile",
    "src.apps.website",
    "src.apps.storage",
    "src.apps.wishlist",
)

THIRD_PARTY_APPS = ("rest_framework",)

# * Apps specific for this project go here.
LOCAL_APPS = ()

# * See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# * END APP CONFIGURATION

# TODO: should check logging

# * WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "src.core.wsgi.application"
# * END WSGI CONFIGURATION

# TODO: should create the auth user
# # * AUTH USER MODEL CONFIGURATION
AUTH_USER_MODEL = "authentication.User"
# # * END AUTH USER MODEL CONFIGURATION

# * RESTFARMEWORK CONFIGURATION
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "otp_hour": get_env("OTP_HOUR"),
        "otp_day": get_env("OTP_DAY"),
        "like_hour": get_env("LIKE_HOUR"),
        "like_day": get_env("LIKE_DAY"),
        "comment_hour": get_env("COMMENT_HOUR"),
        "comment_day": get_env("COMMENT_DAY"),
    },
    "EXCEPTION_HANDLER": "src.api.exception_handler.api_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "src.apps.authentication.backends.JWTAuthentication",
    ),
}
# * END RESTFARMEWORK CONFIGURATION

# * JWT CONFIGURATION
ACCESS_TTL = int(get_env("ACCESS_TTL"))
REFRESH_TTL = int(get_env("REFRESH_TTL"))
JWT_SECRET = get_env("JWT_SECRET")

redis_loc = get_env("REDIS_URL").split(",")
if len(redis_loc) == 1:
    redis_loc = redis_loc[0]
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_loc,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": get_env("REDIS_PASSWORD", optional=True),
        },
    }
}

# DEVELOPMENT MODE CONFIGURATION
UNDER_DEVELOPMENT = get_env("UNDER_DEVELOPMENT", default="False") == "True"
# END DEVELOPMENT MODE CONFIGURATION

# OTP CONFIGURATION
OTP_CODE_LENGTH = int(get_env("OTP_CODE_LENGTH"))
OTP_TTL = int(get_env("OTP_TTL"))
FORGET_PASSWORD_PREFIX = get_env("FORGET_PASSWORD_PREFIX", default="forget_password:")
# END OTP CONFIGURATION

########## NATS CONFIGURATION
SMS_SUBJECT = get_env("SMS_SUBJECT", default="winkie.send_sms")
SMS_STREAM = get_env("SMS_STREAM", default="WINKIE")
NATS_CLUSTER_ID = get_env("NATS_CLUSTER_ID")
NATS_URL = get_env("NATS_URL")
########## END NATS CONFIGURATION
