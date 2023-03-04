from django.core.validators import MinLengthValidator
from rest_framework import serializers
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
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = models.User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'image', 'last_login')
        extra_kwargs = {
            'first_name':{
                'required':False
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

# class UserUpdateImageSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.User
#         fields = ('image',)


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email',None)
        if not email:
            raise exceptions.FieldRequired(['Field email required'])
        try:
            models.User.objects.get(email=email)
        except:
            raise exceptions.UserNotFound
        return attrs


class UserResetPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(max_length=130,required=True,validators=[MinLengthValidator(8)])
    code = serializers.CharField(max_length=20,required=True)


    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])


class UserDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('password',)



class UserBasicSerializer(TokensSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'last_login', 'image', 'email', 'access', 'refresh')
