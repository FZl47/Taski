from django.core.validators import MinLengthValidator
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core import exceptions
from core.serializers import BaseSerializer
from . import models


class Token:
    class GetAccess(BaseSerializer, serializers.Serializer):
        access = serializers.CharField(max_length=350)
        pass

    class GetRefresh(BaseSerializer, serializers.Serializer):
        refresh = serializers.CharField(max_length=350)

    class Get(BaseSerializer, serializers.Serializer):
        access = serializers.SerializerMethodField('get_token_access', read_only=True)
        refresh = serializers.SerializerMethodField('get_token_refresh', read_only=True)

        def get_token_access(self, user):
            return user.get_token_access()

        def get_token_refresh(self, user):
            return user.get_token_refresh()

    class GetAccessByRefresh(BaseSerializer, TokenRefreshSerializer):
        pass


class User:
    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.User
            fields = ('first_name', 'last_name', 'image', 'email', 'password')
            extra_kwargs = {
                'image': {
                    'required': False
                },
                'password': {
                    'validators': [
                        MinLengthValidator(8)
                    ]
                }
            }

        def create(self, validated_data):
            user = models.User(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            image = validated_data.get('image')
            if image:
                user.image = image
            user.set_password(validated_data['password'])
            user.save()
            return user

    class Create(Token.Get):
        pass

    class GetBasic(Token.Get, ModelSerializer):
        image = serializers.URLField(source='get_image')

        class Meta:
            model = models.User
            fields = (
                'id', 'first_name', 'last_name', 'last_login', 'image', 'email', 'access', 'refresh')

    class GetID(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.User
            fields = ('id',)

    class GroupList(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.User
            fields = ('groups_task',)

    class UpdateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.User
            fields = ('first_name', 'last_name', 'image')
            extra_kwargs = {
                'first_name': {
                    'required': False
                },
                'last_name': {
                    'required': False
                },
                'image': {
                    'required': False
                },
                'last_login': {
                    'required': False
                }
            }

    class Update(UpdateRequestBody):
        pass

    class ResetPasswordRequestBody(BaseSerializer, serializers.Serializer):
        email = serializers.EmailField(required=True)

        def validate(self, attrs):
            email = attrs.get('email', None)
            if not email:
                raise exceptions.FieldRequired(['Field email required'])
            try:
                models.User.objects.get(email=email)
            except:
                raise exceptions.UserNotFound
            return attrs

    class ResetPasswordCodeRequestBody(BaseSerializer, serializers.Serializer):
        email = serializers.EmailField(required=True)
        new_password = serializers.CharField(max_length=130, required=True, validators=[MinLengthValidator(8)])
        code = serializers.CharField(max_length=20, required=True)

        def update(self, instance, validated_data):
            instance.set_password(validated_data['new_password'])

    class DeleteRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.User
            fields = ('password',)


class Group:
    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Group
            fields = ('title',)

    class Create(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Group
            fields = ('id', 'title')

    class Get(BaseSerializer, ModelSerializer):
        members = User.GetID(source='user_set', read_only=True, many=True)

        class Meta:
            model = models.Group
            fields = ('id', 'title', 'datetime_created', 'members')

    class Delete(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Group
            fields = ('id', 'title')


class GroupUser:
    class AddUserRequestBody(BaseSerializer, serializers.Serializer):
        email = serializers.EmailField()

    class AddUser(BaseSerializer, serializers.Serializer):
        message = serializers.CharField()

    class AcceptRequestJoin(BaseSerializer, ModelSerializer):
        group_id = serializers.CharField(source='group.id', read_only=True)
        group_title = serializers.CharField(source='group.title', read_only=True)

        class Meta:
            model = models.RequestUserToJoinGroup
            fields = ('user', 'group_title', 'group_id')

    class List(User.GetID):
        pass

    class Kick(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Group
            fields = ('id',)


class GroupAdmin:
    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.GroupAdmin
            fields = ('user', 'group_id')

    class Create(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.GroupAdmin
            fields = ('id',)
            extra_kwargs = {
                'id': {
                    'help_text': 'ID admin'
                }
            }

    class Get(BaseSerializer, ModelSerializer):
        id = serializers.CharField(source='user.id')
        first_name = serializers.CharField(source='user.first_name')
        last_name = serializers.CharField(source='user.last_name')

        class Meta:
            model = models.GroupAdmin
            fields = ('id', 'first_name', 'last_name')

    class Kick(BaseSerializer, ModelSerializer):
        group_id = serializers.CharField(source='group.id')

        class Meta:
            model = models.GroupAdmin
            fields = ('group_id',)
