"""
Production settings.
"""

from .settings_base import *  # noqa: F403,F401


DEBUG = False

_allowed_hosts = os.getenv("ALLOWED_HOSTS", "")  # noqa: F405
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts.split(",") if h.strip()]

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost"]

CORS_ALLOW_ALL_ORIGINS = False  # noqa: F405
