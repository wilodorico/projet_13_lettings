"""
Local/Development settings for oc_lettings_site project.

These settings are optimized for development with debug mode enabled.
"""

import os

import sentry_sdk

from .base import *  # noqa

# ----------------------------------------
# Debug and Security
# ----------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]


# ----------------------------------------
# Sentry - Optional in development
# ----------------------------------------
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        enable_tracing=True,
    )

# ----------------------------------------
# Logging - Development configuration
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
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",  # noqa: F405
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
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "oc_lettings_site": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "letting": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "profiles": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
