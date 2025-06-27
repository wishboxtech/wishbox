"""Development settings and globals."""

from settings.common import *

# * DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
# * END DEBUG CONFIGURATION


# *  EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# * END EMAIL CONFIGURATION


# * TOOLBAR CONFIGURATION
INSTALLED_APPS += ("debug_toolbar",)
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
# * END TOOLBAR CONFIGURATION

# SWAGGER
ENABLE_SWAGGER = get_env("ENABLE_SWAGGER", default=False) == "True"
# END SWAGGER
