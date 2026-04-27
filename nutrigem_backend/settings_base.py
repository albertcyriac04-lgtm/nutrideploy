"""
Django settings for nutrigem_backend project.
Optimized for Vercel Deployment & MCA Standards.
"""

import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. BASE DIRECTORY & PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
# Adding 'apps' directory to sys.path for cleaner imports
sys.path.insert(0, str(BASE_DIR / "apps"))

# Load environment variables from .env
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

# 2. SECURITY SETTINGS
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-fallback-key-for-dev-only")

# Set DEBUG based on environment variable
DEBUG = os.getenv("DEBUG", "True") == "True"

# Configure Allowed Hosts for Vercel and Local Development
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'nutrideploy.vercel.app',
    '.vercel.app',  # Allows all Vercel deployment subdomains
]

# 3. APPLICATION DEFINITION
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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files in production
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

# 4. DATABASE CONFIGURATION
# Uses dj_database_url to parse the Neon/Postgres connection string
DATABASES = {
    "default": dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 5. PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 6. INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 7. STATIC AND MEDIA FILES
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage for efficient serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 8. CROSS-ORIGIN RESOURCE SHARING (CORS) & CSRF
CORS_ALLOW_CREDENTIALS = True

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://nutrideploy.vercel.app",
        # Add your React/Vite frontend URL here
    ]
    # Important for Django 4.0+
    CSRF_TRUSTED_ORIGINS = ["https://nutrideploy.vercel.app"]

# 9. PROXY & HTTPS SETTINGS (Required for Vercel)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 10. REST FRAMEWORK & THIRD-PARTY APIs
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# 11. EMAIL SETTINGS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f'NutriDiet <{os.getenv("EMAIL_HOST_USER")}>'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
