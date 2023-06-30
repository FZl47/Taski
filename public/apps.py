from django.apps import AppConfig


class PublicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'public'

    def ready(self):
        # init tasks

        # set crontab for clean Schedule tasks
        from django.db.utils import OperationalError
        from django_q.models import Schedule
        try:
            _, _ = Schedule.objects.get_or_create(
                name='task_clean_schedule_tasks',
                func='core.tasks.delete_old_schedule_task',
                schedule_type='W',  # Weekly period
                repeats=-1  # run forever
            )
        except OperationalError as e:
            # table model is not created
            # 1: Quit the server
            # 2: run "python manage.py migrate" command
            pass
