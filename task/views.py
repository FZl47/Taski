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
from . import serializers


class TaskList(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'get': {
                'title': 'Get Tasks',
                'description': 'get user tasks',
                'query_serializer':serializers.TaskListViewParameterSerializer,
                'responses': {
                    200: serializers.TaskSerializer(many=True)
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated,)

    def get(self, request, group_id):
        user = request.user
        group = get_object_or_none(account_models.Group,id=group_id,user__id__in=[user.id])
        if group is None:
            raise exceptions.NotFound(['Group object not found'])
        tasks = user.task_set.filter(group__id__in=[group.id])
        sort_by = request.query_params.get('sort_by','latest')
        match sort_by:
            case 'latest':
                tasks = tasks.order_by('-id')
            case 'oldest':
                tasks = tasks.order_by('id')
            case 'expire_date_desc':
                tasks = tasks.order_by('-timeleft')
            case 'expire_date_asc':
                tasks = tasks.order_by('timeleft')

        return Response(serializers.TaskSerializer(tasks,many=True).data)


class CreateTask(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'post': {
                'title': 'Create Task',
                'description': 'create task for users',
                'request_body': serializers.CreateTaskSerializer,
                'responses': {
                    200: serializers.CreateTaskSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)

    def post(self, request, group_id):
        data = request.data.copy() # add group value field
        data.update({
            'group':group_id,
            'create_by':request.admin.id
        })
        s = serializers.CreateTaskSerializer(data=data)
        if s.is_valid():
            s.save()
        else:
            raise exceptions.BadRequest(exceptions.get_errors_serializer(s))
        return Response(s.data)


class CreateTaskFile(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'post': {
                'title': 'Create Task Attach File',
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

