from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core import exceptions
from account import models as account_models
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


class GetGroupUsersSerializer(ModelSerializer):

    class Meta:
        model = account_models.User
        fields = ('id','first_name','last_name','image')


class DeleteGroupUserSerializer(ModelSerializer):

    class Meta:
        model = account_models.User
        fields = ('id','first_name','last_name','image','email')


class GetGroupAdminsSerializer(ModelSerializer):
    id = serializers.CharField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = models.GroupAdmin
        fields = ('id','first_name','last_name')


class DeleteGroupAdminSerializer(GetGroupAdminsSerializer):
    pass


class AddUserToGroupSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AddUserToGroupResponseSerializer(ModelSerializer):

    class Meta:
        model = account_models.User
        fields = ('id','first_name','last_name','email')
