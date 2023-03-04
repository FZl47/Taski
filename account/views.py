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
from core import redis_py
from . import serializers
from . import models



USER_CONF = {
    "TIMEOUT_RESET_PASSWORD_CODE": 400, # Second
    "KEY_REDIS_RESET_PASSWORD":"RESET_PASSWORD_{}"
}



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
    parser_classes = (parsers.MultiPartParser,)
    def post(self, request):
        s = serializers.UserRegisterSerializer(data=request.data)
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
        },
        required=[
            'username',
            'password'
        ]
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
        data = request.data
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
        s = TokenRefreshSerializer(data=request.data)
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
    parser_classes = (parsers.MultiPartParser,)
    def put(self, request):
        usr = request.user
        s = serializers.UserUpdateSerializer(usr,data=request.data)
        is_valid = s.is_valid()
        if is_valid == False:
            raise exceptions.BadRequest
        else:
            s.update(usr,s.validated_data)
        return Response(serializers.UserUpdateSerializer(usr).data)




class ResetPassword(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'post': {
                'title': 'Reset Password',
                'description': 'Reset password account',
                'request_body': serializers.UserResetPasswordSerializer,
                'responses': {
                    200: openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                        'message':openapi.Schema(type=openapi.TYPE_STRING)
                    })
                },
            },
        }
    }

    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        """
            This endpoint create a random code
            and set it to redis and sent to email.
        """
        s = serializers.UserResetPasswordSerializer(data=request.data)
        if s.is_valid():
            email = s.validated_data['email']
            key_redis = USER_CONF['KEY_REDIS_RESET_PASSWORD'].format(email)
            # Check the code has been sent to this email or not
            past_code = redis_py.get_value(key_redis)
            if past_code == None:
                code = utils.random_num()
                # set code in redis
                redis_py.set_value_expire(key_redis,code,USER_CONF['TIMEOUT_RESET_PASSWORD_CODE'])
                # sent code to email in bg proccess
                subject = 'Reset Password Taski'
                message_email = "Reset Password Taski : {}".format(code)
                utils.send_email(subject,message_email,[email])
                message = 'The password reset code has been sent to your email.'
            else:
                raise exceptions.Conflict(['The password reset code has already been sent to you !'])
            return Response({'message':message})
        raise exceptions.BadRequest



class ResetPasswordCode(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Account'],
        'methods': {
            'post': {
                'title': 'Reset Password Code',
                'description': 'To reset your password, you need to send the code you received from the email to this endpoint',
                'request_body': serializers.UserResetPasswordCodeSerializer,
                'responses': {
                    200: openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                        'message':openapi.Schema(type=openapi.TYPE_STRING)
                    })
                },
            },
        }
    }

    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        """
            This endpoint get code reset
            and check and set new password.
        """
        s = serializers.UserResetPasswordCodeSerializer(data=request.data)
        if s.is_valid():
            email = s.validated_data['email']
            code = s.validated_data['code']
            key_redis = USER_CONF['KEY_REDIS_RESET_PASSWORD'].format(email)
            # Check the code has been sent to this email or not
            code_redis = redis_py.get_value(key_redis)
            if code_redis:
                # check codes
                if str(code) == str(code_redis):
                    try:
                        # get user and set new password
                        usr = models.User.objects.get(email=email)
                        s.update(usr,s.validated_data)
                        message = 'Your password has been successfully changed'
                        # remove code in redis
                        redis_py.remove_key(key_redis)
                    except:
                        # user not found
                        raise exceptions.UserNotFound
                else:
                    # codes reset not match
                    raise exceptions.InvalidCode
            else:
                # code reset has expired
                raise exceptions.InvalidCode(['The reset code has expired or invalid !'])
            return Response({'message':message})
        raise exceptions.BadRequest(exceptions.serializer_err(s))

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
        s = serializers.UserDeleteSerializer(usr,data=request.data)
        is_valid = s.is_valid()
        # Check password user
        if is_valid and usr.check_password(s.validated_data['password']):
            # Delete User or anything ..
            usr.delete()
        else:
            raise exceptions.InvalidField(['Password is incorrect'])
        return Response({'message':'Bye...'})