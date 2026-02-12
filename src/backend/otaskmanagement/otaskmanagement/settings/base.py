from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------------------------------------ #
# Core / Security (Defaults safe for loading, strict in Prod)
# ------------------------------------------------------------------ #

ALLOWED_HOSTS: list = []
CSRF_TRUSTED_ORIGINS: list = []

# ------------------------------------------------------------------ #
# Applications
# ------------------------------------------------------------------ #
DJANGO_SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

ALLAUTH_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework.authtoken",
    "corsheaders",
    "celery",
    "django_celery_beat",
]

PROJECT_APPS = [
    "users",
    "project",
    "issues",
    "common",
]

INSTALLED_APPS = DJANGO_SYSTEM_APPS + ALLAUTH_APPS + THIRD_PARTY_APPS + PROJECT_APPS

SITE_ID = 1
AUTH_USER_MODEL = "users.CustomUser"
PROJECT_APP_LABELS = {app.split(".")[-1] for app in PROJECT_APPS}

# ------------------------------------------------------------------ #
# Middleware
# ------------------------------------------------------------------ #
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------------------------ #
# Authentication & Passwords
# ------------------------------------------------------------------ #
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------ #
# DRF / SimpleJWT (Base Config)
# ------------------------------------------------------------------ #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": True,
    "REGISTER_SERIALIZER": "users.serializers.UserRegisterSerializer",
}
DJ_REST_AUTH = {"TOKEN_MODEL": None}
REST_AUTH_TOKEN_MODEL = None

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_OBTAIN_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenObtainPairSerializer"
    ),
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# ------------------------------------------------------------------ #
# Celery
# ------------------------------------------------------------------ #
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# ------------------------------------------------------------------ #
# I18n / Static / Templates
# ------------------------------------------------------------------ #
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

ROOT_URLCONF = "otaskmanagement.urls"
WSGI_APPLICATION = "otaskmanagement.wsgi.application"

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

# ------------------------------------------------------------------ #
# Email (Default to Console to prevent silent failures in dev)
# ------------------------------------------------------------------ #
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
