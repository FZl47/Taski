from django.contrib.auth import get_user_model
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


class CreateAdminGroupSerializer(ModelSerializer):
    class Meta:
        model = models.GroupAdmin
        fields = ('user',)



class CreateAdminResponseGroupSerializer(ModelSerializer):
    class Meta:
        model = models.GroupAdmin
        fields = ('id',)
        extra_kwargs = {
            'id':{
                'help_text':'ID admin'
            }
        }



class AddAdminToGroupSerializer(ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id','admins')
        extra_kwargs = {
            'id':{
                'read_only':True,
                'help_text':'ID group'
            },
            'admins':{
                'required':True
            }
        }


class GetAdminGroupSerializer(ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id','admins')
        extra_kwargs = {
            'id':{
                'read_only':True,
                'help_text':'ID group'
            },
            'admins':{
                'required':True
            }
        }

