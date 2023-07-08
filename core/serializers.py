from rest_framework import serializers
from rest_framework.fields import empty
from .utils import random_num
from . import exceptions


class BaseSerializer(serializers.Serializer):

    def __init__(self, instance=None, data=empty, **kwargs):
        super(BaseSerializer, self).__init__(instance=instance, data=data, **kwargs)
        """
            Fix error:
            drf_yasg.errors.SwaggerGenerationError(because they implicitly share the same ref_name;
            explicitly set the ref_name attribute on both serializers' Meta classes)
            conflict :
                Task.Get => "Get"
                TaskResponse.Get => "Get"
                that is same name method for prevent this add 'ref_name' to 'Meta' class
        """
        meta_class = getattr(self.__class__, 'Meta', None)
        if meta_class:
            setattr(meta_class, 'ref_name', f"{meta_class.model.__name__}_{random_num(10)}")

    def is_valid(self, *, raise_exception=True):
        # raise exception default value True for raise custom style err
        try:
            super(BaseSerializer, self).is_valid(raise_exception=raise_exception)
        except Exception as e:
            # handle error with custom style
            if raise_exception:
                raise exceptions.BadRequest(exceptions.get_errors_serializer(self))
        else:
            pass
