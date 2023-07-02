import uuid
from django.db import models
from core.exceptions import NotFound


class BaseModelMixin(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def get_obj(cls, model_name='__MODEL__', **kwargs):
        obj = get_object_or_none(cls, **kwargs)
        if obj is None:
            if model_name == '__MODEL__':
                model_name = cls.__name__
                model_name = ''.join(' ' + x if x.isupper() else x for x in model_name).strip(' ')
            raise NotFound([f"{model_name} object not found"])
        return obj

    @classmethod
    def get_objects(cls, **kwargs):
        return cls.objects.filter(**kwargs)


def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
