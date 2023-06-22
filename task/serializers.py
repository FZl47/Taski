from rest_framework.serializers import ModelSerializer
from . import models


class TaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        exclude = ('group','users')


class CreateTaskSerializer(ModelSerializer):

    class Meta:
        model = models.Task
        exclude = ('group',)


class CreateTaskFileAttachSerializer(ModelSerializer):

    class Meta:
        model = models.TaskFile
        fields = ('file',)




