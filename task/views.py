from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions as permissions_base
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
                'responses': {
                    200: serializers.TaskSerializer
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
        pass


class CreateTaskFile(SwaggerMixin, APIView):
    SWAGGER = {
        'tags': ['Task'],
        'methods': {
            'post': {
                'title': 'Create Task Attach File',
                'description': 'create file attach',
                'request_body': serializers.CreateTaskFileAttachSerializer,
                'responses': {
                    200: serializers.CreateTaskFileAttachSerializer
                },
            },
        }
    }

    permission_classes = (permissions_base.IsAuthenticated, permissions_account.IsOwnerOrAdminGroup,)
    parser_classes = (MultiPartParser,)

    def post(self, request, group_id):
        s = serializers.CreateTaskFileAttachSerializer(data=request.data)
        print(s.is_valid())
