import os
from datetime import timedelta
from typing import Any

import dj_database_url

from . import base

DEBUG = False

# ------------------------------------------------------------------ #
# Security Checks (Fail fast if missing)
# ------------------------------------------------------------------ #
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")

extra_allowed_host = os.getenv("DJANGO_ALLOWED_HOSTS")
if not extra_allowed_host:
    raise RuntimeError("ALLOWED_HOSTS environment variable is required")
ALLOWED_HOSTS = [h.strip() for h in extra_allowed_host.split(",") if h.strip()]

extra_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if not extra_csrf:
    raise RuntimeError("CSRF_TRUSTED_ORIGINS environment variable is required")
CSRF_TRUSTED_ORIGINS = [u.strip() for u in extra_csrf.split(",") if u.strip()]

# ------------------------------------------------------------------ #
# Database
# ------------------------------------------------------------------ #
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
    )
}

# ------------------------------------------------------------------ #
# Static Files (Whitenoise)
# ------------------------------------------------------------------ #
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------------------------------------------ #
# CORS
# ------------------------------------------------------------------ #
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    u.strip() for u in os.getenv("FRONTEND_BASE_URL", "").split(",") if u
]

# ------------------------------------------------------------------ #
# Security Headers
# ------------------------------------------------------------------ #
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# ------------------------------------------------------------------ #
# Celery (Production Limits)
# ------------------------------------------------------------------ #
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_TASK_SOFT_TIME_LIMIT = 2 * 60
CELERY_TASK_TIME_LIMIT = CELERY_TASK_SOFT_TIME_LIMIT + 15

# ------------------------------------------------------------------ #
# JWT (Strict)
# ------------------------------------------------------------------ #
SIMPLE_JWT: dict[str, Any] = base.SIMPLE_JWT.copy()
SIMPLE_JWT.update(
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
        "ROTATE_REFRESH_TOKENS": True,
        "BLACKLIST_AFTER_ROTATION": True,
        "SIGNING_KEY": SECRET_KEY,
    }
)

# ------------------------------------------------------------------ #
# Auth / Allauth (Strict)
# ------------------------------------------------------------------ #
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/5m",
}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["openid", "email", "profile"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        },
    }
}

# ------------------------------------------------------------------ #
# Email
# ------------------------------------------------------------------ #
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() in ("1", "true", "yes", "on")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ------------------------------------------------------------------ #
# Logging
# ------------------------------------------------------------------ #
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
