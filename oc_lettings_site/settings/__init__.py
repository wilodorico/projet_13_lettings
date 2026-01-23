"""
Django settings for oc_lettings_site project.

This module dynamically loads the appropriate settings based on the DJANGO_ENV environment variable.
- DJANGO_ENV=local or dev -> local settings (development) with .env
- DJANGO_ENV=production or prod -> production settings (uses system env vars)
- Default: local settings with .env
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Determine environment first (from system env or default)
DJANGO_ENV = os.getenv("DJANGO_ENV", "local").lower()

# Load .env file ONLY in development
if DJANGO_ENV not in ["production", "prod"]:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    else:
        load_dotenv()  # Fallback to default .env

# Import the appropriate settings module
if DJANGO_ENV in ["production", "prod"]:
    from .production import *  # noqa
else:
    from .local import *  # noqa
