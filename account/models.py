import datetime
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from core import exceptions, validators
from core.models import BaseModelMixin
from core.mixins.model.delete_file import RemovePastFileMixin


@validators.decorators.validator_image_format
def upload_image_user(instance, path):
    """
        return src file in media
    """
    path = str(path).split('.')[-1]
    instance_email = str(instance.email).replace('.', '_')
    return f"images/users/{instance_email}/{get_random_string(10)}.{path}"


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(BaseModelMixin, RemovePastFileMixin, AbstractUser):
    """
        Custom User Model
    """
    FIELDS_REMOVE_FILES = ['image']

    username = None
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(upload_to=upload_image_user, null=True, blank=True, max_length=300)
    groups_task = models.ManyToManyField('Group')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)

    def get_token_access(self):
        return str(RefreshToken.for_user(self).access_token)

    def get_token_refresh(self):
        return str(RefreshToken.for_user(self))

    def get_image(self):
        if self.image:
            return settings.GET_FULL_HOST(self.image.url)


class RequestUserToJoinGroup(BaseModelMixin, models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    expire_after_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        now = datetime.datetime.now()
        if now < (self.datetime_created + datetime.timedelta(days=self.expire_after_days)):
            return True
        return False

    def __str__(self):
        return f"Request Join To Group - user:{self.user} group:{self.group}"



class HistoryActionGroup(BaseModelMixin, models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    admin = models.ForeignKey('GroupAdmin', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"#{self.id} History action Group - {self.title[:20]}.."


class Group(BaseModelMixin, models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class GroupAdmin(BaseModelMixin, models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"# {self.user} - Group : {self.group}"
