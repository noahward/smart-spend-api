import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# Environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "port": env("DB_PORT"),
    }
}

CORS_ALLOW_ALL_ORIGINS = True

# Sentry logging
sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(
            transaction_style="url",
            middleware_spans=True,
            signals_spans=False,
        ),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment="development",
)
