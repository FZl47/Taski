import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'create first admin'

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.filter(is_superuser=True).first()
        if user:
            username = os.environ['DJANGO_SUPERUSER_USERNAME']
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL','')
            password = os.environ['DJANGO_SUPERUSER_PASSWORD']
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        else:
            print('ERROR : superuser(admin) is exists')


