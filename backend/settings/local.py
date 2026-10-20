"""Local full-stack settings, separate from production and existing .env files."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env.local")
from settings.dev import *

SECRET_KEY = os.environ["SECRET_KEY"]
MEDIA_ROOT = str(BASE_DIR / os.environ.get("MEDIA_ROOT", "media"))
STATIC_ROOT = str(BASE_DIR / os.environ.get("STATIC_ROOT", "static"))
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
CSRF_TRUSTED_ORIGINS = [
    f"http://{host}:{port}"
    for host in ("localhost", "127.0.0.1")
    for port in {
        os.environ.get("WEB_PORT", "8080"),
        os.environ.get("API_PORT", "8000"),
        "5173",
    }
]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# The toolbar probes host.docker.internal on every request. Linux Docker may
# spend minutes resolving that optional hostname; the SPA does not use the toolbar.
MIDDLEWARE = tuple(
    item
    for item in MIDDLEWARE
    if item != "debug_toolbar.middleware.DebugToolbarMiddleware"
)
