from django_q.models import Schedule


def delete_old_schedule_task():
    Schedule.objects.filter(
        repeats=0, # select useless schedule task
    ).delete()