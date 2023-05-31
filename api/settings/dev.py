import os
import logging

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *

# Environment variables
env = environ.Env(USE_SENTRY=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "port": env("DB_PORT"),
    }
}

CORS_ALLOW_ALL_ORIGINS = True

if env("USE_SENTRY"):
    sentry_logging = LoggingIntegration(
        level=logging.DEBUG,  # Capture debug info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )

    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[
            DjangoIntegration(
                transaction_style="url",
                middleware_spans=True,
                signals_spans=False,
            ),
            sentry_logging,
        ],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment="development",
    )
