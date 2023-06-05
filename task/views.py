from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions, parsers
from core.mixins.view.swagger import SwaggerMixin
from core import exceptions
from core.response import Response
from core.models import get_object_or_none
from account import models as account_models
from . import permissions as task_permissions
from . import serializers
from . import models


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

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        s = serializers.CreateGroupSerializer(user, data=request.data)
        is_valid = s.is_valid()
        if is_valid:
            title = s.validated_data['title']
            group = models.Group.objects.create(title=title, owner=user)
            user.groups_task.add(group)
        else:
            messages = exceptions.get_errors_serializer(s.errors)
            raise exceptions.FieldRequired(messages)
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

    permission_classes = (permissions.IsAuthenticated, task_permissions.IsOwnerGroup)

    def delete(self, request, group_id):
        group = getattr(request,'group')
        response_data = serializers.DeleteGroupSerializer(group).data
        group.delete()
        return Response(response_data)


class AddUserToGroup(SwaggerMixin, APIView):

    SWAGGER = {
        'tags': ['Group'],
        'methods': {
            'post': {
                'title': 'Add User to Group',
                'description': 'add user(member) to group',
                'request_body':serializers.AddUserToGroupSerializer,
                'responses': {
                    200: serializers.AddUserToGroupResponseSerializer,
                },
            },
        }
    }

    permission_classes = (permissions.IsAuthenticated,task_permissions.IsOwnerOrAdminGroup)

    def post(self, request, group_id):
        group = getattr(request,'group')
        s = serializers.AddUserToGroupSerializer(data=request.data)
        if s.is_valid():
            email = s.data['email']
            user = get_object_or_none(account_models.User,email=email)
            if user is None:
                raise exceptions.UserNotFound
            # TODO:should send email to accept request join
            user.groups_task.add(group)
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s.errors))
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

    permission_classes = (permissions.IsAuthenticated,)

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

    permission_classes = (permissions.IsAuthenticated,task_permissions.IsOwnerOrAdminGroup)

    def delete(self, request, group_id,user_id):
        group = getattr(request,'group')
        user = get_object_or_none(account_models.User,id=user_id,groups_task__in=[group.id])
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

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, group_id):
        group = get_object_or_none(models.Group,id=group_id)
        if group is None:
            raise exceptions.NotFound(['Group not found'])
        response_data = serializers.GetGroupAdminsSerializer(group.admins,many=True).data
        return Response(response_data)


class CreateAdminGroup(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group Admin'],
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

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = serializers.CreateAdminGroupSerializer(data=request.data)
        if s.is_valid():
            admin_group = s.save()
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s.errors))
        return Response(serializers.CreateAdminResponseGroupSerializer(admin_group).data)


class AddAdminToGroup(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group Admin'],
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

    permission_classes = (permissions.IsAuthenticated, task_permissions.IsOwnerGroup)

    def put(self, request, group_id):
        group = getattr(request,'group')
        s = serializers.AddAdminToGroupSerializer(group,request.data)
        if s.is_valid():
            admins = s.validated_data['admins']
            # add admins to group
            group.admins.add(*admins)
            # add admins to users group
            for admin in admins:
                admin.user.groups_task.add(group)
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s.errors))
        return Response(serializers.AddAdminToGroupSerializer(group).data)


class DeleteGroupAdmin(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Group Admin'],
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

    permission_classes = (permissions.IsAuthenticated, task_permissions.IsOwnerGroup)

    def delete(self, request, group_id,admin_id):
        group = getattr(request,'group')
        admin = get_object_or_none(models.GroupAdmin,id=admin_id,group__id=group_id)
        if admin is None:
            raise exceptions.NotFound(['Admin not found'])
        group.admins.remove(admin)
        response_data = serializers.DeleteGroupAdminSerializer(admin).data
        return Response(response_data)



# class GetAdminGroup(SwaggerMixin, APIView):
#     SWAGGER = {
#         'tags': ['Group Admin'],
#         'methods': {
#             'get': {
#                 'title': 'Get Admin',
#                 'description': 'get information admin group',
#                 'request_body': serializers.GetAdminGroupSerializer,
#                 'responses': {
#                     200: serializers.GetAdminGroupSerializer
#                 },
#             },
#         }
#     }
#
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, group_id):
#         pass

