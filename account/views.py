from django.core import validators
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework import permissions as permissions_base, parsers
from rest_framework_simplejwt.tokens import RefreshToken
from core.response import Response
from core.views import BaseView
from core import utils, redis_py, exceptions
from . import serializers, models, permissions, swagger

USER_RESET_PASSWORD_CONF = settings.USER_RESET_PASSWORD_CONF


class User(BaseView):
    VIEW_NAMES = (
        'Create', 'Login', 'UpdateLogin', 'UpdateUser',
        'ResetPassword', 'ResetPasswordCode', 'Delete',
        'GroupList'
    )
    SWAGGER = swagger.User

    class Create(APIView):
        permission_classes = (permissions_base.AllowAny,)
        parser_classes = (parsers.MultiPartParser,)

        def post(self, request):
            s = serializers.User.CreateRequestBody(data=request.data)
            s.is_valid()
            # save new user
            user = s.save()
            # create a group for user (default group - personal group)
            group = models.Group.objects.create(title='Personal group')
            owner = models.GroupAdmin.objects.create(user=user, is_owner=True, group=group)
            user.groups_task.add(group)
            return Response(serializers.User.Create(user).data)

    class Login(APIView):
        permission_classes = (permissions_base.AllowAny,)

        def post(self, request):
            data = request.data
            email = data.get('username')
            password = data.get('password')
            try:
                validators.EmailValidator()(email)
            except validators.ValidationError:
                raise exceptions.InvalidEmail
            try:
                validate_password(password)
            except:
                raise exceptions.InvalidField(['Please enter password correctly'])
            user = authenticate(request, email=email, password=password)
            if user is None:
                raise exceptions.UserNotFound
            # update last login time
            user.last_login = utils.get_datetime_f()
            user.save()
            return Response(serializers.User.GetBasic(user).data)

    class UpdateLogin(APIView):
        permission_classes = (permissions_base.AllowAny,)

        def put(self, request):
            s = serializers.Token.GetRefresh(data=request.data)
            s.is_valid()
            refresh = s.validated_data['refresh']
            try:
                access = RefreshToken(refresh).access_token
            except:
                raise exceptions.InvalidToken

            return Response(serializers.Token.GetAccess({'access': access}).data)

    class UpdateUser(APIView):
        parser_classes = (parsers.MultiPartParser,)

        def put(self, request):
            user = request.user
            s = serializers.User.UpdateRequestBody(user, data=request.data)
            s.is_valid()
            s.update(user, s.validated_data)
            return Response(serializers.User.Update(user).data)

    class ResetPassword(APIView):
        permission_classes = (permissions_base.AllowAny,)

        def post(self, request):
            """
                This view create a random code
                and set it to redis and sent to email.
            """
            s = serializers.User.ResetPasswordRequestBody(data=request.data)
            s.is_valid()
            email = s.validated_data['email']
            key_redis = USER_RESET_PASSWORD_CONF['KEY_REDIS_RESET_PASSWORD'].format(email)
            # Check the code has been sent to this email or not
            code_past = redis_py.get_value(key_redis)
            if code_past is not None:
                raise exceptions.Conflict(['The password reset code has already been sent to you !'])
            code = utils.random_num()
            # set code in redis
            redis_py.set_value_expire(key_redis, code, USER_RESET_PASSWORD_CONF['TIMEOUT_RESET_PASSWORD_CODE'])
            # sent code to email in bg process
            subject = 'Reset Password Taski'
            message_email = "Reset Password Taski : {}".format(code)
            utils.send_email(subject, message_email, [email])
            return Response({'message': 'The password reset code has been sent to your email.'})

    class ResetPasswordCode(APIView):
        permission_classes = (permissions_base.AllowAny,)

        def post(self, request):
            """
                This endpoint get code reset
                and check and set new password.
            """
            s = serializers.User.ResetPasswordCodeRequestBody(data=request.data)
            s.is_valid()
            email = s.validated_data['email']
            code = s.validated_data['code']
            key_redis = USER_RESET_PASSWORD_CONF['KEY_REDIS_RESET_PASSWORD'].format(email)
            # Check the code has been sent to this email or not
            code_redis = redis_py.get_value(key_redis)

            if not code_redis:
                # code reset has expired
                raise exceptions.InvalidCode(['The reset code has expired or invalid'])

            # check codes
            if str(code) != str(code_redis):
                # codes reset not match
                raise exceptions.InvalidCode

            user = models.User.get_obj(email=email, raise_err=False)
            if user is None:
                # user not found
                raise exceptions.UserNotFound(['User not found with this email'])

            s.update(user, s.validated_data)
            # remove code in redis
            redis_py.remove_key(key_redis)
            return Response({'message': 'Your password has been successfully changed'})

    class Delete(APIView):
        def delete(self, request):
            user = request.user
            s = serializers.User.DeleteRequestBody(user, data=request.data)
            s.is_valid()
            # Check password user
            if user.check_password(s.validated_data['password']) is False:
                raise exceptions.InvalidField(['Password is incorrect'])
            # Delete User
            user.delete()
            return Response({'message': 'Bye Friend...'})

    class GroupList(APIView):
        def get(self, request):
            user = request.user
            return Response(serializers.User.GroupList(user).data)


class Group(BaseView):
    VIEW_NAMES = (
        'Create',
        'Retrieve',
        'Delete'
    )
    SWAGGER = swagger.Group

    class Create(APIView):
        def post(self, request):
            user = request.user
            s = serializers.Group.CreateRequestBody(user, data=request.data)
            s.is_valid()
            title = s.validated_data['title']
            group = models.Group.objects.create(title=title)
            owner = models.GroupAdmin.objects.create(user=user, is_owner=True, group=group)
            user.groups_task.add(group)
            return Response(serializers.Group.Create(group).data)

    class Retrieve(APIView):
        def get(self, request, group_id):
            group = models.Group.get_obj(id=group_id)
            return Response(serializers.Group.Get(group).data)

    class Delete(APIView):
        use_child_permission = True
        permission_classes_additional = (permissions.IsOwnerGroup,)

        def delete(self, request, group_id):
            # get group from user by "permissions.IsOwnerGroup"
            group = request.group
            response_data = serializers.Group.Delete(group).data
            group.delete()
            return Response(response_data)


class GroupUser(BaseView):
    VIEW_NAMES = (
        'RequestAddUser',
        'AcceptRequestJoin',
        'List',
        'Kick'
    )
    permission_classes_additional = (permissions.IsOwnerOrAdminGroup,)
    SWAGGER = swagger.GroupUser

    class RequestAddUser(APIView):
        def post(self, request, group_id):
            group = request.group
            s = serializers.GroupUser.AddUserRequestBody(data=request.data)
            s.is_valid()
            email = s.data['email']
            user = models.User.get_obj(email=email)
            models.RequestUserToJoinGroup.objects.create(user=user, group=group)
            models.HistoryActionGroup.objects.create(
                title='Request Join',
                user=user,
                group=group,
                admin=request.admin
            )
            return Response(serializers.GroupUser.AddUser({'message':'Request join to group sent'}).data)

    class AcceptRequestJoin(APIView):
        use_child_permission = True
        permission_classes = (permissions_base.AllowAny,)

        def get(self, request, token):
            obj = models.RequestUserToJoinGroup.get_obj(token=token)
            if obj.is_active is False:
                raise exceptions.UserNotFound(['Request Join object is not active'])
            if obj.is_valid() is False:
                raise exceptions.InvalidField(['Token is expired!'])
            user = request.user
            group = request.group
            user.groups_task.add(group)
            obj.is_active = False
            obj.save()
            return Response(serializers.GroupUser.AcceptRequestJoin(obj).data)

    class List(APIView):
        def get(self, request, group_id):
            group = models.Group.get_obj(id=group_id)
            users = group.user_set.all()
            return Response(serializers.GroupUser.List(users,many=True).data)

    class Kick(APIView):
        def delete(self, request, group_id, user_id):
            group = request.group
            admin = request.admin
            user = models.User.get_obj(id=user_id, groups_task__in=[group.id])
            user.groups_task.remove(group)
            models.HistoryActionGroup.objects.create(
                title=f'Kick user',
                group=group,
                admin=admin,
                user=user,
                description=f'Kick user #{user.id}|{user.email}'
                            f'from {group.title} by #{admin.id}|{admin.user.email}'
            )
            return Response(serializers.GroupUser.Kick(user).data)


class GroupAdmin(BaseView):
    VIEW_NAMES = (
        'Create',
        'List',
        'Delete'
    )
    SWAGGER = swagger.GroupAdmin
    permission_classes_additional = (permissions.IsOwnerGroup,)

    class Create(APIView):
        def post(self, request, group_id):
            s = serializers.GroupAdmin.CreateRequestBody(request.group, request.data)
            s.is_valid()
            admin_group = s.save()
            admin_group.user.groups_task.add(request.group)
            return Response(serializers.GroupAdmin.Create(admin_group).data)

    class List(APIView):
        use_child_permission = True
        permission_classes = (permissions_base.IsAuthenticated,)
        def get(self, request, group_id):
            group = models.Group.get_obj(id=group_id)
            return Response(serializers.GroupAdmin.Get(group.admins, many=True).data)

    class Delete(APIView):
        use_child_permission = True
        permission_classes = (permissions_base.IsAuthenticated, permissions.IsOwnerGroup)

        def delete(self, request, group_id, admin_id):
            group = request.group
            admin = models.GroupAdmin.get_obj(id=admin_id, group__id=group_id, is_owner=False)
            group.admins.remove(admin)
            return Response(serializers.GroupAdmin.Kick(admin).data)


