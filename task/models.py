import uuid
from django.db import models
from core import validators

@validators.decorators.validator_file_format
def upload_src_task_file(instance,path):
    """
        :return src task file in media
    """
    instance_id = instance.pk or get_random_string(13)
    return f"files/task/{instance_id}/{get_random_string(10)}.{path}"


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('account.User',on_delete=models.CASCADE)
    admins = models.ManyToManyField('GroupAdmin',blank=True)


class GroupAdmin(models.Model):
    user = models.ForeignKey('account.User',on_delete=models.CASCADE)



class Task(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    users = models.ManyToManyField('account.User')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    attach = models.ManyToManyField('TaskFile')
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
    timeleft = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"#{self.group_id} - {self.title[:30]}"


class TaskFile(models.Model):
    file = models.FileField(upload_to=upload_src_task_file)




