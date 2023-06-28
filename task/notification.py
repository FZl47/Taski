from django.template.loader import render_to_string
from core.utils import send_email_html
from core.models import get_object_or_none
from .models import Task


def send_notify_task_timeleft(task_id,*args,**kwargs):
    task = get_object_or_none(Task,id=task_id)
    if task:
        context = {
            'task': task,
            'type_period_time':kwargs.get('type_period_time')
        }
        res_html = render_to_string('public/components/notification_task_remind.html', context)
        send_email_html('Remind Task ..', res_html, [task.user.email])
    else:
        # task not found
        pass


def send_notify_task_new(task,**kwargs):
    context = {
        'task':task
    }
    res_html = render_to_string('public/components/notification_newtask.html',context)
    send_email_html('New Task !',res_html,[task.user.email])