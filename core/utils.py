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


def get_datetime_div(dt_start, dt_end, div):
    """
        return division on datetime
    """
    assert div <= 100
    dt = dt_end - dt_start
    tm = dt / div
    res = dt_end - tm
    return res


def get_days_hours_minutes_td(td) -> tuple:
    """
        return days hours and minutes from timedelta object
    """
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60


def send_email(subject: str, message: str, email_receiver: list):
    """
        send email in background
    """
    email_from = settings.EMAIL_HOST_USER
    async_task(_send_email_django, (subject, message, email_from, email_receiver))


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
