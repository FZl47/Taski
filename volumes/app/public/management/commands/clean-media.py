import shutil, os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'clean all media files'

    def handle(self, *args, **options):
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
            self.stdout.write(
                self.style.SUCCESS('Directory media cleaned as successfully!')
            )
            os.mkdir(settings.MEDIA_ROOT)
        except Exception as e:
            raise CommandError(e)


