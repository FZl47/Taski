from django.db import models
from django.utils.crypto import get_random_string
from core import validators
from core.models import BaseModelMixin


@validators.decorators.validator_file_format
def upload_src_task_file(instance,path):
    """
        return src task file in media
    """
    instance_id = instance.pk or get_random_string(13)
    return f"files/task/{instance_id}/{get_random_string(10)}.{path}"


class Task(BaseModelMixin,models.Model):
    group = models.ForeignKey('account.Group',on_delete=models.CASCADE)
    users = models.ManyToManyField('account.User')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    attach = models.ManyToManyField('TaskFile')
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
    timeleft = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"#{self.group_id} - {self.title[:30]}"


class TaskFile(BaseModelMixin,models.Model):
    file = models.FileField(upload_to=upload_src_task_file)




