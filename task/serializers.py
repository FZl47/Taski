from rest_framework.serializers import ModelSerializer
from core import exceptions
from . import models



class CreateGroupSerializer(ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id','title')
        extra_kwargs = {
            'id':{
                'read_only':True
            }
        }


class DeleteGroupSerializer(ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id','title')
        extra_kwargs = {
            'title':{
                'read_only':True
            }
        }


