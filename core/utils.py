import datetime
import random
from django.core.mail import send_mail as _send_email_django, EmailMultiAlternatives
from django.conf import settings
from django_q.tasks import async_task



def get_datetime():
    """
        return datetime
    """
    return datetime.datetime.now()


def get_datetime_f(f='%Y-%m-%d %H:%M:%S'):
    """
        return datetime with custom format time
    """
    return get_datetime().strftime(f)


def get_datetime_div(dt, div):
    """
        return division on datetime
    """
    tm = datetime.timedelta(days=dt.day, minutes=dt.minute, seconds=dt.second)
    tm = tm / div
    assert div <= 100
    dt = dt - tm
    return dt


def send_email(subject: str, message: str, email_receiver: list):
    """
        send email in background
    """
    email_from = settings.EMAIL_HOST_USER
    async_task(_send_email_django,(subject, message, email_from, email_receiver))


def send_email_html(subject: str, message: str, email_receiver: list):
    email_from = settings.EMAIL_HOST_USER
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=email_from,
        to=email_receiver
    )
    email.attach_alternative(message, "text/html")
    async_task(email.send)


def random_num(n=6):
    """
        create random number
    """
    return ''.join(random.choices('123456789', k=n))
