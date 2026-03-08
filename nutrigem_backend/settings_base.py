"""
Base Django settings shared across all environments.
"""

from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import os
import sys

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "apps"))
load_dotenv(dotenv_path=BASE_DIR / ".env")


SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this-in-production")


INSTALLED_APPS = [
    "admin_app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
    "user_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nutrigem_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nutrigem_backend.wsgi.application"
ASGI_APPLICATION = "nutrigem_backend.asgi.application"


def _database_config_from_url(database_url: str):
    parsed = urlparse(database_url)
    scheme = (parsed.scheme or "").split("+")[0].lower()

    if scheme in ("postgres", "postgresql"):
        engine = "django.db.backends.postgresql"
        default_port = "5432"
    elif scheme in ("mysql", "mysql2"):
        engine = "django.db.backends.mysql"
        default_port = "3306"
    elif scheme == "sqlite":
        engine = "django.db.backends.sqlite3"
        default_port = ""
    else:
        raise ValueError(f"Unsupported DATABASE_URL scheme: {scheme}")

    query = parse_qs(parsed.query)
    options = {k: v[0] for k, v in query.items() if v}

    if engine == "django.db.backends.postgresql" and "sslmode" not in options:
        options["sslmode"] = "require"
    if engine == "django.db.backends.mysql":
        options.setdefault("charset", "utf8mb4")
        options.setdefault("init_command", "SET sql_mode='STRICT_TRANS_TABLES'")

    if engine == "django.db.backends.sqlite3":
        db_name = parsed.path or "/db.sqlite3"
    else:
        db_name = (parsed.path or "").lstrip("/")

    config = {
        "ENGINE": engine,
        "NAME": db_name,
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or default_port),
    }
    if options:
        config["OPTIONS"] = options
    return config


database_url = os.getenv("DATABASE_URL")
if database_url:
    DATABASES = {"default": _database_config_from_url(database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "nutrigem_db"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", "1234"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

LOGIN_URL = "login"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f'NutriDiet <{os.getenv("EMAIL_HOST_USER")}>'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

_csrf_trusted_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_trusted_origins.split(",") if o.strip()]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
