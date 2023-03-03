from django.shortcuts import render
from django.core import validators
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions, parsers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from core.mixins.view.swagger import SwaggerMixin
from core import exceptions
from core.response import Response
from core import utils
from . import serializers


class Register(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'post': {
                'title': 'Create user',
                'description': 'create new account | register ',
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
        if user == None:
            raise exceptions.UserNotFound
        # update last login time
        user.last_login = utils.get_datetime_f()
        user.save()
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
            is_valid = s.is_valid()
        except:
            raise exceptions.InvalidToken(['Refresh token is invalid'])
        if is_valid == False:
            raise exceptions.FieldRequired(['Field refresh is required'])
        return Response(serializers.TokenAccessSerializer(s.validated_data).data)


class UserUpdate(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'put': {
                'title': 'Update user',
                'description': 'Update user information',
                'request_body': serializers.UserUpdateSerializer,
                'responses': {
                    200: serializers.UserUpdateSerializer,
                },
            },
        }
    }

    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser,)
    def put(self, request):
        usr = request.user
        s = serializers.UserUpdateSerializer(usr,data=request.POST)
        is_valid = s.is_valid()
        if is_valid == False:
            raise exceptions.BadRequest
        else:
            s.update(usr,s.validated_data)
        return Response(serializers.UserUpdateSerializer(usr).data)


# class UserUpdateImage(SwaggerMixin, APIView):
#     SWAGGER = {
#         'tags': ['Account'],
#         'methods': {
#             'put': {
#                 'title': 'Update user image',
#                 'description': 'Update user image information',
#                 'request_body': serializers.UserUpdateImageSerializer,
#                 'responses': {
#                     200: serializers.UserUpdateImageSerializer,
#                 },
#             },
#         }
#     }
#
#     permission_classes = (permissions.IsAuthenticated,)
#     parser_classes = (parsers.MultiPartParser,)
#
#     def put(self, request):
#         usr = request.user
#         s = serializers.UserUpdateImageSerializer(usr,data=request.FILES)
#         is_valid = s.is_valid()
#         if is_valid == False:
#             raise exceptions.BadRequest
#         else:
#             s.update(usr,s.validated_data)
#         return Response(serializers.UserUpdateImageSerializer(usr).data)


class UserDelete(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'delete': {
                'title': 'Delete User',
                'description': 'Delete user account',
                'request_body': serializers.UserDeleteSerializer,
                'responses': {
                    200: openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                        'message':openapi.Schema(type=openapi.TYPE_STRING,default='Bye...')
                    })
                },
            },
        }
    }

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        usr = request.user
        s = serializers.UserDeleteSerializer(usr,data=request.POST)
        is_valid = s.is_valid()
        # Check password user
        if is_valid == False and usr.check_password(s.validated_data['password']):
            raise exceptions.InvalidField(['Password is incorrect'])
        else:
            # Delete User or anything ..
            usr.delete()
        return Response({'message':'Bye...'})