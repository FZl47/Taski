"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

STAGE = {
    'dev': 'config.settings.development',  # Development
    'prod': 'config.settings.production'  # Production
}
stage_state = os.environ.get('stage_state','dev')
SETTINGS = STAGE[stage_state]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS)

application = get_wsgi_application()
