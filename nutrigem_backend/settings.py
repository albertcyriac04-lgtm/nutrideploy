"""
Compatibility settings entrypoint.

Use DJANGO_ENV=production for production settings.
Defaults to local settings for development.
"""

import os


DJANGO_ENV = os.getenv("DJANGO_ENV", "local").strip().lower()

if DJANGO_ENV == "production":
    from .settings_production import *  # noqa: F403,F401
else:
    from .settings_local import *  # noqa: F403,F401
