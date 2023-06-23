from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models


class TaskListViewParameterSerializer(serializers.Serializer):
    SORT_BY_OPTIONS = (
        ('latest', 'default'),
        ('oldest', 'Oldest'),
        ('expire_date_desc', 'later expiration date'),
        ('expire_date_asc', 'closer expiration date'),
    )
    sort_by = serializers.ChoiceField(SORT_BY_OPTIONS, default=SORT_BY_OPTIONS[0][0])


class CreateTaskFileAttachSerializer(ModelSerializer):

    class Meta:
        model = models.TaskFile
        fields = ('file', 'task')


class CreateTaskFileAttachResponseSerializer(ModelSerializer):
    file = serializers.URLField(source='get_file')

    class Meta:
        model = models.TaskFile
        fields = ('id','file', 'task')


class GetTaskFileAttachSerializer(ModelSerializer):
    file = serializers.URLField(source='get_file')

    class Meta:
        model = models.TaskFile
        fields = ('id','file')


class CreateTaskSerializer(ModelSerializer):

    class Meta:
        model = models.Task
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    attach = GetTaskFileAttachSerializer(many=True, source='taskfile_set', read_only=True)

    class Meta:
        model = models.Task
        exclude = ('group', 'users')