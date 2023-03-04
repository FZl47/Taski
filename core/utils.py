import datetime
import random
from django.core.mail import send_mail as _send_email_django
from django.conf import settings
from core.task_bg import Thread, Task

_Thread = Thread()

def get_datetime():
    """
        this function return datetime
    """
    return datetime.datetime.now()

def get_datetime_f():
    """
        this function return datetime with custom format time
    """
    return get_datetime().strftime('%Y-%m-%d %H:%M:%S')


def send_email(subject:str,message:str,email_receiver:[]):
    """
        send email in background
    """
    email_from = settings.EMAIL_HOST_USER
    t = Task(_send_email_django,args=(subject, message, email_from, email_receiver))
    _Thread.add(t)
    _Thread.start_or_continue()


def random_num(n=6):
    """
        create random number
    """
    return ''.join(random.choices('123456789', k=n))