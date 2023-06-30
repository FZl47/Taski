from functools import wraps
from django.conf import settings as _settings
from core import exceptions


def validator_image_format(func):
    """
        This decorator should use for path function
        like : ImageField(upload_to= this_func )
    """

    @wraps(validator_image_format)
    def wrapper(instance, path, *args, **kwargs):
        path_format = str(path).split('.')[-1]
        if path_format not in _settings.IMAGES_FORMAT:
            raise exceptions.InvalidFormatImage
        return func(instance, path, *args, **kwargs)

    return wrapper


def validator_file_format(func):
    """
        This decorator should use for path function
        like : FileField(upload_to= this_func )
    """

    @wraps(validator_file_format)
    def wrapper(instance, path, *args, **kwargs):
        path_format = str(path).split('.')[-1]
        if path_format not in _settings.FILES_FORMAT:
            raise exceptions.InvalidFormatFile
        return func(instance, path, *args, **kwargs)

    return wrapper
