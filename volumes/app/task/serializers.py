from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from core.serializers import BaseSerializer
from . import models


class TaskResponseFile:
    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponseFile
            fields = ('file',)

    class Create(BaseSerializer, ModelSerializer):
        file = serializers.URLField(source='get_file')

        class Meta:
            model = models.TaskResponseFile
            fields = ('id', 'file', 'task_response', 'datetime_created', 'datetime_updated')

    class UpdateRequestBody(CreateRequestBody):
        pass

    class Update(BaseSerializer, ModelSerializer):
        file = serializers.URLField(source='get_file')

        class Meta:
            model = models.TaskResponseFile
            fields = ('file', 'datetime_updated')

    class Get(Update):
        pass

    class Delete(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponseFile
            fields = ('task_response',)


class TaskFile:
    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskFile
            fields = ('file', 'task')

    class Create(BaseSerializer, ModelSerializer):
        file = serializers.URLField(source='get_file')

        class Meta:
            model = models.TaskFile
            fields = ('id', 'file', 'task', 'datetime_created', 'datetime_updated')

    class UpdateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskFile
            fields = ('task', 'file')

    class Update(BaseSerializer, ModelSerializer):
        file = serializers.URLField(source='get_file')

        class Meta:
            model = models.TaskFile
            fields = ('id', 'file', 'datetime_updated')

    class Get(BaseSerializer, ModelSerializer):
        file = serializers.URLField(source='get_file')

        class Meta:
            model = models.TaskFile
            fields = ('id', 'file', 'task', 'datetime_created', 'datetime_updated')

    class DeleteRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskFile
            fields = ('task',)

    class Delete(BaseSerializer, ModelSerializer):
        file = serializers.URLField(source='get_file')

        class Meta:
            model = models.TaskFile
            fields = '__all__'


class TaskResponse:
    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponse
            fields = ('task', 'content')

    class Create(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponse
            fields = '__all__'

    class UpdateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponse
            fields = ('content', 'task')

    class Update(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponse
            fields = '__all__'

    class Get(BaseSerializer, ModelSerializer):
        attach = TaskResponseFile.Get(many=True, source='taskresponsefile_set', read_only=True)

        class Meta:
            model = models.TaskResponse
            fields = '__all__'

    class DeleteRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.TaskResponse
            fields = ('task',)

    class Delete(BaseSerializer, ModelSerializer):
        attach_count = serializers.SerializerMethodField()

        class Meta:
            model = models.TaskResponse
            exclude = ('id', 'datetime_created', 'datetime_updated')

        def get_attach_count(self, obj):
            return obj.taskresponsefile_set.count()


class Task:
    class CreateSwagger(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Task
            exclude = ('is_active', 'is_completed', 'group', 'created_by')

    class CreateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Task
            exclude = ('is_active',)

    class Create(CreateRequestBody):
        # just for response swagger
        pass

    class UpdateRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Task
            fields = (
                'title', 'description', 'label', 'timeleft', 'is_completed', 'datetime_created', 'datetime_updated')
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

    class Update(UpdateRequestBody):
        pass

    class ListRequestParameter(serializers.Serializer):
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
                                               help_text="filter tasks by complete state")

    class Get(ModelSerializer):
        attach = TaskFile.Get(many=True, source='taskfile_set', read_only=True)
        expired = serializers.BooleanField(source='is_expired', read_only=True)
        time_late = serializers.CharField(source='get_time_late', read_only=True)

        class Meta:
            model = models.Task
            exclude = ('group',)

    class DeleteRequestBody(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Task
            fields = ('group',)

    class Delete(BaseSerializer, ModelSerializer):
        class Meta:
            model = models.Task
            fields = ('id', 'group')
