from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from core.utils import send_email_html
from .models import RequestUserToJoinGroup


@receiver(post_save,sender=RequestUserToJoinGroup)
def send_email_request_to_join_group(sender,instance,created,**kwargs):
    if created:
        context = {
            'group':instance.group,
            'link_request_accept':settings.GET_FULL_HOST(reverse('account:accept_request_join_group_user',args=(instance.token,)))
        }
        request_content = render_to_string('account/request_join_group.html', context)
        send_email_html('Request Join To Group !', request_content,[instance.user.email])