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
def upload_image_user(instance,path):
    """
        :return src file in media
    """
    # instance_id = instance.pk or get_random_string(13)
    instance_email = str(instance.email).replace('.','_')
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



class User(BaseModelMixin,RemovePastFileMixin,AbstractUser):
    """
        Custom User Model
    """
    FIELDS_REMOVE_FILES = ['image']

    username = None
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_('email address'), unique = True)
    image = models.ImageField(upload_to=upload_image_user,null=True,blank=True)
    groups_task = models.ManyToManyField('task.Group')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
       return "{}".format(self.email)

    def get_token_access(self):
        return str(RefreshToken.for_user(self).access_token)

    def get_token_refresh(self):
        return str(RefreshToken.for_user(self))