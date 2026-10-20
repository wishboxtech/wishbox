"""Isolated test settings; opt into PostgreSQL with WISHBOX_TEST_DB=postgres."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env.test")
from settings.common import *

DEBUG = False
ENABLE_SWAGGER = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
UNDER_DEVELOPMENT = True
MEDIA_ROOT = os.environ.get("WISHBOX_TEST_MEDIA_ROOT", "/tmp/wishbox-test-media")
MEDIA_URL = "/media/"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
CACHES = {
    "default": {"BACKEND": "tests.cache.MemoryTTLCache", "LOCATION": "wishbox-tests"}
}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

if os.environ.get("WISHBOX_TEST_DB") != "postgres":
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    }
