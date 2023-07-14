from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.models import Schedule
from core.utils import get_datetime_div, get_datetime
from .notification import send_notify_task_new
from .models import Task


@receiver(post_save, sender=Task)
def set_scheduler_timeleft_task(sender, instance, created, **kwargs):
    task_schedule_name = instance.get_name_obj_task_schedule_timeleft()
    if created is False:
        # delete old schedule's
        Schedule.objects.filter(name=task_schedule_name).delete()
    else:
        send_notify_task_new(instance)

    timeleft = instance.timeleft
    is_active = instance.is_active
    is_completed = instance.is_completed

    if (timeleft is not None) and (is_completed is False) and is_active:
        # create new schedule's
        schedule_data = {
            'name': task_schedule_name,
            'func': 'task.notification.send_notify_task_timeleft',
            'args':f"'{instance.id}'",
            'schedule_type': 'O',
            'repeats': 1,
        }
        time_now = get_datetime()
        # timeleft expired
        Schedule.objects.create(
            **schedule_data,
            next_run=timeleft,
            kwargs=f"type='notify',type_period_time='expired'"
        )

        # half of the time left
        half_of_timeleft = get_datetime_div(time_now,timeleft, 2)
        if half_of_timeleft > time_now:
            Schedule.objects.create(
                **schedule_data,
                next_run=half_of_timeleft,
                kwargs=f"type='notify',type_period_time='half'"
            )

        # fifth of the time left
        fifth_of_timeleft = get_datetime_div(time_now,timeleft, 5)
        if fifth_of_timeleft > time_now:
            Schedule.objects.create(
                **schedule_data,
                next_run=fifth_of_timeleft,
                kwargs=f"type='notify',type_period_time='fifth'"
            )
