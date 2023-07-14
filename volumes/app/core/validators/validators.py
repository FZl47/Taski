from django.conf import settings
from core.exceptions import FileTooLarge


def limit_file_size(value):
    MAX_UPLOAD_SIZE = int(settings.MAX_UPLOAD_SIZE)
    if value.size > MAX_UPLOAD_SIZE:
        MAX_UPLOAD_SIZE_LABEL = settings.MAX_UPLOAD_SIZE_LABEL
        raise FileTooLarge(f'File too large. Size should not exceed {MAX_UPLOAD_SIZE_LABEL}')


__all__ = ['limit_file_size']