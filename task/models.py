import datetime
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.validators import MinValueValidator
from core import validators
from core.models import BaseModelMixin
from core.mixins.model.delete_file import RemovePastFileMixin


@validators.decorators.validator_file_format
def upload_src_task_file(instance,path):
    """
        return src task file in media
    """
    path = str(path).split('.')[-1]
    return f"files/group/{instance.task.group.id}/task/{instance.task.id}/{get_random_string(10)}.{path}"


class Task(BaseModelMixin,models.Model):
    create_by = models.ForeignKey('account.GroupAdmin',on_delete=models.CASCADE) # TODO : should be complete view and tests
    group = models.ForeignKey('account.Group',on_delete=models.CASCADE)
    users = models.ManyToManyField('account.User')
    title = models.CharField(max_length=200)
    label = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
    timeleft = models.DateTimeField(null=True,blank=True,validators=[MinValueValidator(datetime.datetime.now)])

    def __str__(self):
        return f"#{self.group_id} - {self.title[:30]}"

    def get_users_id(self):
        return list(self.users.all().values_list('id',flat=True))


class TaskFile(BaseModelMixin,RemovePastFileMixin,models.Model):
    FIELDS_REMOVE_FILES = ['file']
    task = models.ForeignKey('Task',on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_src_task_file,max_length=300)
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ATTACH FILE #{self.id} - {self.task.title}"

    def get_file(self):
        return settings.GET_FULL_HOST(self.file.url)




