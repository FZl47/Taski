from collections import namedtuple
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.validators import MinValueValidator
from core import validators, exceptions
from core.models import BaseModelMixin
from core.utils import get_days_hours_minutes_td, get_datetime
from core.mixins.model.delete_file import RemovePastFileMixin


@validators.decorators.validator_file_format
def upload_src_task_file(instance, path):
    """
        return src task file in media
    """
    path = str(path).split('.')[-1]
    return f"files/group/{instance.task.group.id}/task/{instance.task.id}/{get_random_string(10)}.{path}"


class TaskManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get(self,*args,**kwargs):
        try:
            return super().get(is_active=True, *args, **kwargs)
        except:
            raise exceptions.NotFound(['Task not found or is not active'])


class Task(BaseModelMixin, models.Model):
    created_by = models.ForeignKey('account.GroupAdmin', on_delete=models.CASCADE)
    group = models.ForeignKey('account.Group', on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    timeleft = models.DateTimeField(null=True, blank=True, validators=[MinValueValidator(get_datetime)])
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = TaskManager()

    def __str__(self):
        return f"#{self.group_id} - {self.title[:30]}"

    def is_expired(self):
        return True # TODO: should be complete

    def get_time_late(self):
        pass  # TODO: should be complete | return: time late after expiration

    def get_time_left(self):
        td = self.timeleft - get_datetime()
        timeleft = namedtuple('timeleft', ['days', 'hours', 'minutes'])
        return timeleft(*get_days_hours_minutes_td(td))

    def get_name_obj_task_schedule_timeleft(self):
        return f"task_schedule_timeleft_{self.id}"


class FileMixin(RemovePastFileMixin, models.Model):
    FIELDS_REMOVE_FILES = ['file']
    file = models.FileField(upload_to=upload_src_task_file, max_length=300, validators=[validators.limit_file_size],
                            help_text=f'Size file should not exceed {settings.MAX_UPLOAD_SIZE_LABEL}')

    class Meta:
        abstract = True


class TaskFile(BaseModelMixin,FileMixin):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    def __str__(self):
        return f"ATTACH FILE #{self.id} - {self.task}"

    def get_file(self):
        return settings.GET_FULL_HOST(self.file.url)


class TaskResponse(BaseModelMixin, models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Task Response - #{self.id} - {self.task}"


class TaskFileResponse(BaseModelMixin,FileMixin):
    task_response = models.ForeignKey('TaskResponse',on_delete=models.CASCADE)

    def __str__(self):
        return f"# Task File Response - #{self.id} - {self.task_response.task}"