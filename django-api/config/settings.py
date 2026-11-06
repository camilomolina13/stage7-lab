import os
from pathlib import Path

from dotenv import load_dotenv

# django-api/config/settings.py -> BASE_DIR = django-api/
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")          # el .env está en la raíz del repo

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Solo lo que la API necesita: sin admin, auth ni sesiones
INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "tracker",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "project_tracker"),
        "USER": os.getenv("DB_USER", "tracker"),
        "PASSWORD": os.getenv("DB_PASSWORD", "tracker_pass"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True
APPEND_SLASH = False                 # /api/projects, sin slash final

CORS_ALLOW_ALL_ORIGINS = True        # solo para desarrollo

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_CONTENT_NEGOTIATION_CLASS": "tracker.helpers.IgnoreClientContentNegotiation",
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
    "EXCEPTION_HANDLER": "tracker.errors.custom_exception_handler",
}