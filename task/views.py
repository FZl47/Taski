from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions as permissions_base
from drf_yasg import openapi
from core.mixins.view.swagger import SwaggerMixin
from core.models import get_object_or_none
from core import exceptions
from core.response import Response
from account import permissions as permissions_account
from account import models as account_models
from . import serializers, models


class TaskList(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'get': {
                'title': 'Get Tasks',
                'description': 'get user tasks',
                'query_serializer': serializers.TaskListViewParameterSerializer,
                'responses': {
                    200: serializers.TaskSerializer(many=True)
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,permissions_account.IsMemberShip)

    def get(self, request, group_id):
        group = request.group
        user = request.user
        tasks = user.task_set.filter(group__id__in=[group.id])
        is_completed_param = request.query_params.get('is_completed','all')
        match is_completed_param:
            case True:
                tasks = tasks.filter(is_completed=True)
            case False:
                tasks = tasks.filter(is_completed=False)
            case _:
                # default all tasks
                pass
        sort_by = request.query_params.get('sort_by', 'latest')
        match sort_by:
            case 'latest':
                tasks = tasks.order_by('-id')
            case 'oldest':
                tasks = tasks.order_by('id')
            case 'expire_date_desc':
                tasks = tasks.order_by('-timeleft')
            case 'expire_date_asc':
                tasks = tasks.order_by('timeleft')

        return Response(serializers.TaskSerializer(tasks, many=True).data)


class CreateTask(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'post': {
                'title': 'Create Task',
                'description': 'create task for user',
                'request_body': serializers.CreateTaskRequestBodySerializer,
                'responses': {
                    200: serializers.CreateTaskSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)

    def post(self, request, group_id):
        data = request.data.copy()  # add group value field
        data.update({
            'group': group_id,
            'created_by': request.admin.id
        })
        s = serializers.CreateTaskSerializer(data=data)
        if s.is_valid():
            s.save()
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(s.data)


class DeleteTask(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'delete': {
                'title': 'Delete Task',
                'description': 'delete task',
                'responses': {
                    200: serializers.DeleteTaskSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)

    def delete(self, request, group_id, task_id):
        data = {
            'group': group_id,
        }
        s = serializers.DeleteTaskSerializer(data=data)
        if s.is_valid():
            task_obj = get_object_or_none(models.Task, id=task_id, group_id=group_id)
            if task_obj is None:
                raise exceptions.NotFound(['Task not found'])
            response_serializer = serializers.DeleteTaskSerializer(task_obj).data
            task_obj.delete()
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(response_serializer)


class UpdateTask(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'put': {
                'title': 'Update Task',
                'description': 'update task',
                'request_body': serializers.UpdateTaskSerializer,
                'responses': {
                    200: serializers.UpdateTaskSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)

    def put(self, request, group_id, task_id):
        task_obj = get_object_or_none(models.Task, id=task_id, group_id=group_id)
        if task_obj is None:
            raise exceptions.NotFound(['Task not found'])
        s = serializers.UpdateTaskSerializer(instance=task_obj, data=request.data)
        if s.is_valid():
            task_obj = s.update(task_obj, s.validated_data)
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(serializers.UpdateTaskSerializer(task_obj).data)


# class UpdateUsersTask(SwaggerMixin, APIView):
#     SWAGGER = {
#         'tags': ['Task'],
#         'methods': {
#             'put': {
#                 'title': 'Update Users Task',
#                 'description': 'update users task',
#                 'request_body': serializers.UpdateUsersTaskSerializer,
#                 'responses': {
#                     200: serializers.UpdateUsersTaskSerializer
#                 },
#             },
#         }
#     }
#
#     permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)
#
#     def put(self, request, group_id, task_id):
#         task_obj = get_object_or_none(models.Task, id=task_id, group_id=group_id)
#         if task_obj is None:
#             raise exceptions.NotFound(['Task not found'])
#         s = serializers.UpdateUsersTaskSerializer(instance=task_obj, data=request.data)
#         if s.is_valid() is False:
#             raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
#         # check all users are members of the group
#         users = s.validated_data['users']
#         users_in_group = task_obj.group.user_set.filter(email__in=users).count() == len(users)
#         if users_in_group is False:
#             raise exceptions.PermissionDenied(['Cannot assign a task to user|users not a member of the group'])
#         task_obj = s.update(task_obj, s.validated_data)
#         return Response(serializers.UpdateUsersTaskSerializer(task_obj).data)


class CreateTaskFile(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'post': {
                'title': 'Create Attach File Task',
                'description': 'create file attach',
                'request_body': serializers.CreateTaskFileAttachSerializer,
                'responses': {
                    200: serializers.CreateTaskFileAttachResponseSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)
    parser_classes = (MultiPartParser,)

    def post(self, request, group_id):
        s = serializers.CreateTaskFileAttachSerializer(data=request.data)
        if s.is_valid():
            task_file_obj = s.save()
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(serializers.CreateTaskFileAttachResponseSerializer(task_file_obj).data)


class UpdateTaskFile(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'put': {
                'title': 'Update Attach File Task',
                'description': 'update file attach',
                'request_body': serializers.UpdateTaskFileAttachSerializer,
                'responses': {
                    200: serializers.UpdateTaskFileAttachResponseSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)
    parser_classes = (MultiPartParser,)

    def put(self, request, group_id, task_id, task_file_id):
        s = serializers.UpdateTaskFileAttachSerializer(data=request.data)
        task_file_obj = get_object_or_none(models.TaskFile, id=task_file_id, task_id=task_id, task__group__id=group_id)
        if task_file_obj is None:
            raise exceptions.NotFound(['Task file not found'])
        if s.is_valid():
            s.update(task_file_obj,s.validated_data)
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(serializers.UpdateTaskFileAttachResponseSerializer(task_file_obj).data)


class GetTaskFile(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'get': {
                'title': 'Get Attach File Task',
                'description': 'get file attach',
                'responses': {
                    200: serializers.GetTaskFileAttachSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,permissions_account.IsMemberShip)
    parser_classes = (MultiPartParser,)

    def get(self, request, group_id, task_id, task_file_id):
        task_file_obj = get_object_or_none(models.TaskFile, id=task_file_id, task_id=task_id, task__group__id=group_id)
        if task_file_obj is None:
            raise exceptions.NotFound(['Task file not found'])
        return Response(serializers.GetTaskFileAttachSerializer(task_file_obj).data)


class DeleteTaskFile(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'delete': {
                'title': 'Delete Attach File Task',
                'description': 'delete file attach',
                'responses': {
                    200: serializers.DeleteTaskFileAttachSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)

    def delete(self, request, group_id, task_id, task_file_id):
        task_file_obj = get_object_or_none(models.TaskFile,id=task_file_id,task_id=task_id,task__group__id=group_id)
        if task_file_obj:
            task_file_obj.delete()
        else:
            raise exceptions.NotFound(['Task file not found'])
        return Response(serializers.DeleteTaskFileAttachSerializer(task_file_obj).data)
