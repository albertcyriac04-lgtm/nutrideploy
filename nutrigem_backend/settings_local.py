"""
Local development settings.
"""

from .settings_base import *  # noqa: F403,F401


DEBUG = os.getenv("DEBUG", "True") == "True"  # noqa: F405
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

# Convenience for local frontend development.
CORS_ALLOW_ALL_ORIGINS = DEBUG  # noqa: F405
