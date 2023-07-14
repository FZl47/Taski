from .base import *

DEBUG = False

ALLOWED_HOSTS = ['taski.fzlm.ir','app-webserver']  # for now

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

STATIC_ROOT = BASE_DIR.parent / 'assets/static'
MEDIA_ROOT = BASE_DIR.parent / 'assets/media'


