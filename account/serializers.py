from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core import exceptions
from . import models


class TokenAccessSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=350)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=350)


class TokensSerializer(serializers.Serializer):
    access = serializers.SerializerMethodField('get_token_access', read_only=True)
    refresh = serializers.SerializerMethodField('get_token_refresh', read_only=True)

    def get_token_access(self, usr):
        return usr.get_token_access()

    def get_token_refresh(self, usr):
        return usr.get_token_refresh()


class UserRegisterSerializer(serializers.ModelSerializer):
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


class UserUpdateSerializer(serializers.ModelSerializer):
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


class UserResetPasswordSerializer(serializers.Serializer):
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


class UserResetPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(max_length=130, required=True, validators=[MinLengthValidator(8)])
    code = serializers.CharField(max_length=20, required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('password',)


class UserBasicSerializer(TokensSerializer, serializers.ModelSerializer):
    image = serializers.URLField(source='get_image')

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'last_login', 'image', 'email', 'access', 'refresh', 'groups_task')


class AcceptRequestJoinToGroupResponseSerializer(serializers.ModelSerializer):
    group_id = serializers.CharField(source='group.id', read_only=True)
    group_title = serializers.CharField(source='group.title', read_only=True)

    class Meta:
        model = models.RequestUserToJoinGroup
        fields = ('user', 'group_title', 'group_id')


class CreateGroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'title')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class DeleteGroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'title')
        extra_kwargs = {
            'title': {
                'read_only': True
            }
        }


class CreateAdminGroupSerializer(ModelSerializer):
    class Meta:
        model = models.GroupAdmin
        fields = ('user', 'group_id')


class CreateAdminResponseGroupSerializer(ModelSerializer):
    class Meta:
        model = models.GroupAdmin
        fields = ('id',)
        extra_kwargs = {
            'id': {
                'help_text': 'ID admin'
            }
        }


class AddAdminToGroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'admins')
        extra_kwargs = {
            'id': {
                'read_only': True,
                'help_text': 'ID group'
            },
            'admins': {
                'required': True
            }
        }


class GetAdminGroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'admins')
        extra_kwargs = {
            'id': {
                'read_only': True,
                'help_text': 'ID group'
            },
            'admins': {
                'required': True
            }
        }


class GetGroupUsersSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'image')


class DeleteGroupUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'image', 'email')


class GetGroupAdminsSerializer(ModelSerializer):
    id = serializers.CharField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = models.GroupAdmin
        fields = ('id', 'first_name', 'last_name')


class DeleteGroupAdminSerializer(GetGroupAdminsSerializer):
    pass


class AddUserToGroupSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AddUserToGroupResponseSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'email')


class GroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'
