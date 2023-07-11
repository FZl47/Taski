import uuid
from django.db import models
from core.exceptions import NotFound


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def get_obj(cls, label_name='__MODEL__', raise_err=True, **kwargs):
        obj = get_object_or_none(cls, **kwargs)
        if label_name == '__MODEL__':
            label_name = cls.__name__
            label_name = ''.join(' ' + x if x.isupper() else x for x in label_name).strip(' ')
        if obj is None and raise_err:
            raise NotFound([f"{label_name.lower()} object not found"])
        return obj

    @classmethod
    def get_objects(cls, **kwargs):
        return cls.objects.filter(**kwargs)


def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
