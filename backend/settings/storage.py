"""Environment-driven media storage shared by local and production runtimes."""

from collections.abc import Mapping
from urllib.parse import urlsplit


def env_bool(env: Mapping[str, str], key: str, default: bool = False) -> bool:
    value = env.get(key, str(default)).strip().lower()
    if value in {"true", "1", "yes", "on"}:
        return True
    if value in {"false", "0", "no", "off", ""}:
        return False
    raise ValueError(f"{key} must be a boolean")


def media_storage_settings(env: Mapping[str, str]) -> dict:
    """Keep static files local; optionally send uploaded media to S3."""
    storages = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
    if not env_bool(env, "USE_S3"):
        return storages

    def setting(key, legacy=None):
        return env.get(key, "").strip() or (
            env.get(legacy, "").strip() if legacy else ""
        )

    endpoint = setting("S3_ENDPOINT_URL", "MINIO_STORAGE_ENDPOINT")
    if endpoint and "://" not in endpoint:
        scheme = "https" if env_bool(env, "MINIO_STORAGE_USE_HTTPS", True) else "http"
        endpoint = f"{scheme}://{endpoint}"
    bucket = setting("S3_BUCKET_NAME", "MINIO_STORAGE_MEDIA_BUCKET_NAME")
    # Older deployments called the bucket name S3_MEDIA_URL.
    if not bucket:
        bucket = env.get("S3_MEDIA_URL", "").strip()
    required = {
        "S3_ENDPOINT_URL": endpoint,
        "S3_BUCKET_NAME": bucket,
        "S3_ACCESS_KEY_ID": setting("S3_ACCESS_KEY_ID", "MINIO_STORAGE_ACCESS_KEY"),
        "S3_SECRET_ACCESS_KEY": setting(
            "S3_SECRET_ACCESS_KEY", "MINIO_STORAGE_SECRET_KEY"
        ),
        "S3_REGION_NAME": setting("S3_REGION_NAME"),
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError("USE_S3 requires: " + ", ".join(missing))
    parts = urlsplit(endpoint)
    if (
        parts.scheme not in {"https", "http"}
        or not parts.netloc
        or parts.username
        or parts.password
        or parts.path.strip("/")
        or parts.query
        or parts.fragment
    ):
        raise ValueError(
            "S3_ENDPOINT_URL must be the service URL, without a bucket or credentials"
        )
    if "/" in bucket or ":" in bucket:
        raise ValueError("S3_BUCKET_NAME must be a bucket name, not a URL")
    addressing_style = env.get("S3_ADDRESSING_STYLE", "path").strip()
    if addressing_style not in {"path", "virtual", "auto"}:
        raise ValueError("S3_ADDRESSING_STYLE must be path, virtual or auto")
    signed = env_bool(env, "S3_QUERYSTRING_AUTH", True)
    custom_domain = env.get("S3_CUSTOM_DOMAIN", "").strip()
    if custom_domain and (
        "://" in custom_domain or "/" in custom_domain or "?" in custom_domain
    ):
        raise ValueError("S3_CUSTOM_DOMAIN must be a hostname without a scheme or path")
    if custom_domain and signed:
        raise ValueError(
            "S3_CUSTOM_DOMAIN requires public media (S3_QUERYSTRING_AUTH=False)"
        )
    expires = int(env.get("S3_QUERYSTRING_EXPIRE", "3600"))
    if expires <= 0:
        raise ValueError("S3_QUERYSTRING_EXPIRE must be positive")
    storages["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": endpoint.rstrip("/"),
            "region_name": required["S3_REGION_NAME"],
            "bucket_name": bucket,
            "access_key": required["S3_ACCESS_KEY_ID"],
            "secret_key": required["S3_SECRET_ACCESS_KEY"],
            "signature_version": "s3v4",
            "addressing_style": addressing_style,
            "querystring_auth": signed,
            "querystring_expire": expires,
            "custom_domain": custom_domain or None,
            "url_protocol": "https:",
            "location": env.get("S3_LOCATION", "").strip("/"),
            "default_acl": None,
            "file_overwrite": False,
            "max_memory_size": 2 * 1024 * 1024,
        },
    }
    return storages
