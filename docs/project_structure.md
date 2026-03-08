# Project Structure

This project now follows a cleaner Django layout used in production teams.

## Core layout

- `apps/`
  - `api/` API models, serializers, viewsets, admin, commands
  - `user_app/` user-facing views and logic
  - `admin_app/` custom admin site/dashboard
- `nutrigem_backend/`
  - `settings_base.py` shared settings
  - `settings_local.py` local/dev overrides
  - `settings_production.py` production overrides
  - `settings.py` environment selector (`DJANGO_ENV`)
  - `urls.py`, `asgi.py`, `wsgi.py`
- `templates/` global Django templates
- `static/` source static assets
- `staticfiles/` collected static output
- `docs/` project docs and conventions
- `backups/` generated database backup files

## Environment strategy

- `DJANGO_ENV=local` -> uses `settings_local.py`
- `DJANGO_ENV=production` -> uses `settings_production.py`
- `DATABASE_URL` preferred for production-grade DB config.
- If `DATABASE_URL` is missing, MySQL env vars (`DB_*`) are used.

## Why this is better

- Clear separation between shared and environment-specific settings.
- Easier production deployment and safer defaults.
- Better onboarding: config is predictable and documented.
