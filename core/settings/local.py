from .base import *  # noqa
from .base import env

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-wj@@x+fhk^_%0)k5nkj$777-2+9wl)1ctw5d1r$w*ype!q^3=o"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", True)

# CORS_URLS_REGEX = r"^api/.*$"

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost:3000',
]

CORS_ALLOW_CREDENTIALS = True

# TODO: Change "Core"
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@tiktok-clone.site"
DEFAULT_NO_REPLY_EMAIL = "no-reply@tiktok-clone.site"
DOMAIN = env("DOMAIN")
SITE_NAME = "TikTok Clone"



