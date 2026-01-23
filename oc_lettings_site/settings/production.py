"""
Production settings for oc_lettings_site project.

These settings are optimized for production deployment with security hardening.
"""

import os

import dj_database_url

from .base import *  # noqa

# ----------------------------------------
# Debug and Security
# ----------------------------------------
DEBUG = False

# ALLOWED_HOSTS must be set via environment variable in production
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"


# Enable when behind HTTPS reverse proxy
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ----------------------------------------
# Static Files (CSS, JavaScript, Images)
# ----------------------------------------
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
STATIC_URL = "/static/"

# WhiteNoise configuration for serving static files
STORAGE_BACKEND = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Must be after SecurityMiddleware
] + [m for m in MIDDLEWARE if m != "django.middleware.security.SecurityMiddleware"]  # noqa: F405

# ----------------------------------------
# Database - PostgreSQL via DATABASE_URL
# ----------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required in production")

DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}


# ----------------------------------------
# Sentry - Optional in production
# ----------------------------------------
SENTRY_DSN = os.getenv("SENTRY_DSN", "").strip()
if SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.1,  # Lower sample rate in production
        send_default_pii=False,  # Don't send PII in production
        environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
        enable_tracing=True,
    )

# ----------------------------------------
# Logging - Production configuration
# ----------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "[{levelname}] {message}", "style": "{"},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",  # noqa: F405
            "formatter": "verbose",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django_errors.log",  # noqa: F405
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file_error"],
            "level": "ERROR",
            "propagate": False,
        },
        "oc_lettings_site": {
            "handlers": ["console", "file", "file_error"],
            "level": "INFO",
            "propagate": False,
        },
        "letting": {
            "handlers": ["console", "file", "file_error"],
            "level": "INFO",
            "propagate": False,
        },
        "profiles": {
            "handlers": ["console", "file", "file_error"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
