from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # init tasks

        # set crontab for clean Schedule tasks
        from django_q.models import Schedule
        Schedule.objects.create(
            name='task_clean_schedule_tasks',
            func='core.tasks.delete_old_schedule_task',
            schedule_type='W', # Weekly period
            repeats=-1 # run forever
        )