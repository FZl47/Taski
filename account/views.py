from django.core import validators
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions as permissions_base , parsers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from core.mixins.view.swagger import SwaggerMixin
from core.response import Response
from core import utils, redis_py, exceptions
from core.models import get_object_or_none
from . import serializers, models, permissions



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

    permission_classes = (permissions_base.AllowAny,)
    parser_classes = (parsers.MultiPartParser,)
    def post(self, request):
        s = serializers.UserRegisterSerializer(data=request.data)
        user = None
        if s.is_valid():
            # save new user
            user = s.save()
            # create a group for user (default group - personal group)
            group = models.Group.objects.create(title='Personal group',owner=user)
            user.groups_task.add(group)
        else:
            errors = exceptions.get_errors_serializer(s)
            raise exceptions.BadRequest(errors)

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

    permission_classes = (permissions_base.AllowAny,)

    def post(self, request):
        # s = serializers.UserBasicSerializer(data=request.data)
        data = request.data
        email = data.get('username')
        password = data.get('password')
        try:
            validators.EmailValidator()(email)
        except validators.ValidationError:
            raise exceptions.InvalidEmail
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
                'title': 'Access Token - Update login',
                'description': 'get access token by refresh token - keep login',
                'request_body': serializers.TokenRefreshSerializer,
                'responses': {
                    200: serializers.TokenAccessSerializer,
                },
            },
        }
    }

    permission_classes = (permissions_base.AllowAny,)

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

    permission_classes = (permissions_base.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)
    def put(self, request):
        user = request.user
        s = serializers.UserUpdateSerializer(user,data=request.data)
        is_valid = s.is_valid()
        if is_valid == False:
            raise exceptions.BadRequest
        else:
            s.update(user,s.validated_data)
        return Response(serializers.UserUpdateSerializer(user).data)


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

    permission_classes = (permissions_base.AllowAny,)
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

    permission_classes = (permissions_base.AllowAny,)
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
                        user = models.User.objects.get(email=email)
                        s.update(user,s.validated_data)
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

    permission_classes = (permissions_base.IsAuthenticated,)

    def delete(self, request):
        user = request.user
        s = serializers.UserDeleteSerializer(user,data=request.data)
        is_valid = s.is_valid()
        # Check password user
        if is_valid and user.check_password(s.validated_data['password']):
            # Delete User or anything ..
            user.delete()
        else:
            raise exceptions.InvalidField(['Password is incorrect'])
        return Response({'message':'Bye...'})


class AcceptRequestGroupJoin(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'get': {
                'title': 'Accept Request Join To Group',
                'description': 'accept request join to group',
                'responses': {
                    200: serializers.AcceptRequestJoinToGroupResponse
                },
            },
        }
    }

    permission_classes = (permissions_base.AllowAny,)

    def get(self, request, token):
        request_obj = get_object_or_none(models.RequestUserToJoinGroup,token=token)
        if request_obj:
            if request_obj.is_valid():
                user = request_obj.user
                group = request_obj.group
                user.groups_task.add(group)
            else:
                raise exceptions.InvalidField(['Token is expired!'])
        else:
            raise exceptions.NotFound(['Token is not valid - request group join not found'])
        s = serializers.AcceptRequestJoinToGroupResponse(request_obj)
        request_obj.delete()
        return Response(s.data)


class CreateGroup(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'post': {
                'title': 'Create Group',
                'description': 'create groups to perform tasks',
                'request_body': serializers.CreateGroupSerializer,
                'responses': {
                    200: serializers.CreateGroupSerializer,
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,)

    def post(self, request):
        user = request.user
        s = serializers.CreateGroupSerializer(user, data=request.data)
        is_valid = s.is_valid()
        if is_valid:
            title = s.validated_data['title']
            group = models.Group.objects.create(title=title, owner=user)
            user.groups_task.add(group)
        else:
            errors = exceptions.get_errors_serializer(s)
            raise exceptions.FieldRequired(errors)
        return Response(serializers.CreateGroupSerializer(group).data)


class DeleteGroup(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'delete': {
                'title': 'Delete Group',
                'description': 'delete group',
                'responses': {
                    200: serializers.DeleteGroupSerializer,
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions.IsOwnerGroup)

    def delete(self, request, group_id):
        group = request.group
        response_data = serializers.DeleteGroupSerializer(group).data
        group.delete()
        return Response(response_data)


class RequestAddUserToGroup(SwaggerMixin, APIView):

    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'post': {
                'title': 'Request Add User to Group',
                'description': 'add user(member) to group',
                'request_body':serializers.AddUserToGroupSerializer,
                'responses': {
                    200: serializers.AddUserToGroupResponseSerializer,
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,permissions.IsOwnerOrAdminGroup)

    def post(self, request, group_id):
        group = request.group
        s = serializers.AddUserToGroupSerializer(data=request.data)
        if s.is_valid():
            email = s.data['email']
            user = get_object_or_none(models.User,email=email)
            if user is None:
                raise exceptions.UserNotFound
            models.RequestUserToJoinGroup.objects.create(user=user,group=group)
            models.HistoryRequestUserToJoinGroup(user=user,group=group,request_by=request.user)
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(serializers.AddUserToGroupResponseSerializer(user).data)


class GroupUsers(SwaggerMixin, APIView):

    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'get': {
                'title': 'Get Users Group',
                'description': 'get users group',
                'responses': {
                    200: serializers.GetGroupUsersSerializer(many=True),
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,)

    def get(self, request, group_id):
        group = get_object_or_none(models.Group,id=group_id)
        if group is None:
            raise exceptions.NotFound(['Group not found'])
        response_data = serializers.GetGroupUsersSerializer(group.user_set.all(),many=True).data
        return Response(response_data)


class DeleteGroupUser(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'delete': {
                'title': 'Delete User Group',
                'description': 'delete user membership group',
                'responses': {
                    200: serializers.DeleteGroupUserSerializer,
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,permissions.IsOwnerOrAdminGroup)

    def delete(self, request, group_id,user_id):
        group = request.group
        user = get_object_or_none(models.User,id=user_id,groups_task__in=[group.id])
        if user is None:
            raise exceptions.NotFound(['User not found'])
        user.groups_task.remove(group)
        response_data = serializers.DeleteGroupUserSerializer(user).data
        return Response(response_data)


class GroupAdmins(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'get': {
                'title': 'Get Admins Group',
                'description': 'get admins group',
                'responses': {
                    200: serializers.GetGroupAdminsSerializer(many=True),
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,)

    def get(self, request, group_id):
        group = get_object_or_none(models.Group,id=group_id)
        if group is None:
            raise exceptions.NotFound(['Group not found'])
        response_data = serializers.GetGroupAdminsSerializer(group.admins,many=True).data
        return Response(response_data)


class CreateAdminGroup(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'post': {
                'title': 'Create Admin',
                'description': 'create an admin for group',
                'request_body': serializers.CreateAdminGroupSerializer,
                'responses': {
                    200: serializers.CreateAdminResponseGroupSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,)

    def post(self, request):
        s = serializers.CreateAdminGroupSerializer(data=request.data)
        if s.is_valid():
            admin_group = s.save()
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(serializers.CreateAdminResponseGroupSerializer(admin_group).data)


class AddAdminToGroup(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'put': {
                'title': 'Add Admin',
                'description': 'add admin to group',
                'request_body': serializers.AddAdminToGroupSerializer,
                'responses': {
                    200: serializers.AddAdminToGroupSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions.IsOwnerGroup)

    def put(self, request, group_id):
        group = request.group
        s = serializers.AddAdminToGroupSerializer(group,request.data)
        if s.is_valid():
            admins = s.validated_data['admins']
            # add admins to group
            group.admins.add(*admins)
            # add admins to users group
            for admin in admins:
                admin.user.groups_task.add(group)
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(serializers.AddAdminToGroupSerializer(group).data)


class DeleteGroupAdmin(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'delete': {
                'title': 'Delete Admin',
                'description': 'delete admin group',
                # 'request_body': serializers.DeleteGroupAdminSerializer,
                'responses': {
                    200: serializers.DeleteGroupAdminSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions.IsOwnerGroup)

    def delete(self, request, group_id,admin_id):
        group = request.group
        admin = get_object_or_none(models.GroupAdmin,id=admin_id,group__id=group_id)
        if admin is None:
            raise exceptions.NotFound(['Admin not found'])
        group.admins.remove(admin)
        response_data = serializers.DeleteGroupAdminSerializer(admin).data
        return Response(response_data)




