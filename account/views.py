from django.shortcuts import render
from django.core import validators
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from core.mixins.view.swagger import SwaggerMixin
from core import exceptions
from core.response import Response
from . import serializers
from django.contrib.auth import get_user_model


class Register(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'post': {
                'title': 'Register',
                'description': 'create new account',
                'request_body': serializers.UserRegisterSerializer,  # serizlier or instance
                'responses': {
                    200: serializers.TokensSerializer,
                },
            },
        }
    }

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = serializers.UserRegisterSerializer(data=request.POST)
        user = None
        if s.is_valid():
            # save new user
            user = s.save()
        else:
            messages = exceptions.get_messages_serializer(s.errors)
            raise exceptions.BadRequest(messages)

        return Response(serializers.TokensSerializer(user).data)


class Login(SwaggerMixin, APIView):

    SWAGGER_SCHEMA_FIELDS = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='your email'
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='your password'
            )
        }
    )

    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'post': {
                'title': 'Login',
                'description': 'login and get basic profile',
                'request_body': SWAGGER_SCHEMA_FIELDS,
                'responses': {
                    200: serializers.UserBasicSerializer,
                },
            },
        }
    }

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.POST
        email = data.get('username')
        password = data.get('password')
        try:
            validators.EmailValidator()(email)
        except validators.ValidationError:
            raise exceptions.InvalidEmail()
        try:
            validate_password(password)
        except :
            raise exceptions.InvalidField(['Please enter password correctly'])
        user = authenticate(request,email=email,password=password)
        return Response(serializers.UserBasicSerializer(user).data)



class AccessToken(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'post': {
                'title': 'Access Token',
                'description': 'get access token by refresh token',
                'request_body': serializers.TokenRefreshSerializer,
                'responses': {
                    200: serializers.TokenAccessSerializer,
                },
            },
        }
    }

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = TokenRefreshSerializer(data=request.POST)
        try:
            s.is_valid()
        except:
            raise exceptions.InvalidToken(['Refresh token is invalid'])
        return Response(serializers.TokenAccessSerializer(s.validated_data).data)