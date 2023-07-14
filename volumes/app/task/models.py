import datetime
from collections import namedtuple
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.validators import MinValueValidator
from core import validators, exceptions
from core.models import BaseModel
from core.utils import get_days_hours_minutes_td, get_datetime
from core.mixins.model.delete_file import RemovePastFileMixin


@validators.decorators.validator_file_format
def upload_src_file(instance, path):
    """
        return src file by datetime in media
    """
    format_file = str(path).split('.')[-1]
    now = datetime.datetime.now()
    return f"files/{now.year}/{now.month}/{now.day}/{get_random_string(14)}.{format_file}"


class TaskManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get(self, *args, **kwargs):
        try:
            return super().get(is_active=True, *args, **kwargs)
        except:
            raise exceptions.NotFound(['Task not found or is not active'])


class Task(BaseModel):
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
        if self.timeleft:
            now = get_datetime()
            return True if now >= self.timeleft else False
        return False

    def get_time_late(self):
        if self.is_expired() is True:
            now = get_datetime()
            time_late = now - self.timeleft
            days, hours, _ = get_days_hours_minutes_td(time_late)
            return '%s days %s minutes' % (days, hours)
        return None

    def get_time_left(self):
        td = self.timeleft - get_datetime()
        timeleft = namedtuple('timeleft', ['days', 'hours', 'minutes'])
        return timeleft(*get_days_hours_minutes_td(td))

    def get_name_obj_task_schedule_timeleft(self):
        return f"task_schedule_timeleft_{self.id}"


class FileModelMixin(RemovePastFileMixin, models.Model):
    FIELDS_REMOVE_FILES = ['file']
    file = models.FileField(upload_to=upload_src_file, max_length=3000, validators=[validators.limit_file_size],
                            help_text=f'size file should not exceed {settings.MAX_UPLOAD_SIZE_LABEL}',null=False)

    class Meta:
        abstract = True

    def get_file(self):
        try:
            return settings.GET_FULL_HOST(self.file.url)
        except:
            raise exceptions.NotFound(['File not found'])


class TaskFile(BaseModel, FileModelMixin):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    def __str__(self):
        return f"ATTACH FILE #{self.id} - {self.task}"


class TaskResponse(BaseModel):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Task Response - #{self.id} - {self.task}"


class TaskResponseFile(BaseModel, FileModelMixin):
    task_response = models.ForeignKey('TaskResponse', on_delete=models.CASCADE)

    def __str__(self):
        return f"Task File Response - #{self.id} - {self.task_response.task}"
