from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*'] # for now

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_production.sqlite3',
    }
}
