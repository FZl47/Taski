from rest_framework import serializers
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


class UserBasicSerializer(TokensSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'image', 'email', 'access', 'refresh')
