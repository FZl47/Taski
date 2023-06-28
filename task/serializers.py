from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

import account.models
from . import models


class TaskListViewParameterSerializer(serializers.Serializer):
    SORT_BY_OPTIONS = (
        ('latest', 'default'),
        ('oldest', 'Oldest'),
        ('expire_date_desc', 'later expiration date'),
        ('expire_date_asc', 'closer expiration date'),
    )
    FILTER_BY_COMPLETE_STATE = (
        ('all', 'default'),
        ('true', 'filter tasks where taks is completed'),
        ('false', 'filter tasks where taks is not completed'),
    )
    sort_by = serializers.ChoiceField(SORT_BY_OPTIONS, default=SORT_BY_OPTIONS[0][0])
    is_completed = serializers.ChoiceField(FILTER_BY_COMPLETE_STATE,
                                           default=FILTER_BY_COMPLETE_STATE[0][0],
                                           help_text="filter tasks by complete state"
                                           )


class CreateTaskFileAttachSerializer(ModelSerializer):
    class Meta:
        model = models.TaskFile
        fields = ('file', 'task')


class CreateTaskFileAttachResponseSerializer(ModelSerializer):
    file = serializers.URLField(source='get_file')

    class Meta:
        model = models.TaskFile
        fields = ('id', 'file', 'task')


class GetTaskFileAttachSerializer(ModelSerializer):
    file = serializers.URLField(source='get_file')

    class Meta:
        model = models.TaskFile
        fields = ('id', 'file')


class UpdateTaskFileAttachSerializer(ModelSerializer):
    class Meta:
        model = models.TaskFile
        fields = ('file',)


class UpdateTaskFileAttachResponseSerializer(ModelSerializer):
    file = serializers.URLField(source='get_file')

    class Meta:
        model = models.TaskFile
        fields = ('id', 'file')


class DeleteTaskFileAttachSerializer(ModelSerializer):
    class Meta:
        model = models.TaskFile
        fields = ('task',)


class CreateTaskRequestBodySerializer(ModelSerializer):
    """
        Just for use in swagger
    """

    class Meta:
        model = models.Task
        exclude = ('is_active', 'group', 'created_by')


class CreateTaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        exclude = ('is_active',)


class TaskSerializer(ModelSerializer):
    attach = GetTaskFileAttachSerializer(many=True, source='taskfile_set', read_only=True)
    expired = serializers.BooleanField(source='is_expired',read_only=True)

    class Meta:
        model = models.Task
        exclude = ('group', 'user')


class DeleteTaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        fields = ('id', 'group')


class UpdateTaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        fields = ('title', 'description', 'label', 'timeleft', 'is_completed', 'datetime_created', 'datetime_updated')
        extra_kwargs = {
            'title': {
                'required': False
            },
            'datetime_created': {
                'read_only': True
            },
            'datetime_updated': {
                'read_only': True
            }
        }

# class UpdateUserTaskSerializer(ModelSerializer):
#     class Meta:
#         model = models.Task
#         fields = ('title', 'user')
#         extra_kwargs = {
#             'title': {
#                 'read_only': True
#             }
#         }
