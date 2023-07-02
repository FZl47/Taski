from rest_framework import serializers
from . import exceptions


class BaseSerializer(serializers.Serializer):

    def is_valid(self, *, raise_exception=True):
        # raise exception default value True for raise custom style err
        try:
            super(BaseSerializer,self).is_valid(raise_exception=raise_exception)
        except Exception as e:
            # handle error with custom style
            if raise_exception:
                raise exceptions.BadRequest(exceptions.get_errors_serializer(self))
        else:
            pass

