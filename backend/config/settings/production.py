import os
from django.core.exceptions import ImproperlyConfigured
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ["DJANGO_ALLOWED_HOSTS"].split(",")
    if host.strip()
]

if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("Production requires explicit allowed hosts.")

CORS_ALLOW_ALL_ORIGINS = [
    origin.strip()
    for origin in os.getenv("DJANGO_CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

# HTTPS security
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

# Enable HSTS after verifying HTTPS deployment.
SECURE_HSTS_SECONDS = 0


API_DOCS_ENABLED = False