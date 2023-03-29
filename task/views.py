from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions, parsers
from core.mixins.view.swagger import SwaggerMixin
from core import exceptions
from core.response import Response
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
            messages = exceptions.get_messages_serializer(s.errors)
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
        response_data =  serializers.DeleteGroupSerializer(group).data
        group.delete()
        return Response(response_data)
