from django.db import models



class Group(models.Model):
    owner = models.ForeignKey('account.User',on_delete=models.CASCADE)
    admins = models.ManyToManyField('GroupAdmin')


class GroupAdmin(models.Model):
    user = models.ForeignKey('account.User',on_delete=models.CASCADE)
    permissions = models.ManyToManyField('Permission')


class Permission(models.Model):
    PERMISSIONS = (
        ('add_user','Add User'),
        ('delete_user','Delete User'),
        ('create_task','Create Task'),
        ('edit_task','Edit Task'),
        ('delete_task','Delete Task'),
    )
    name = models.CharField(max_length=20,choices=PERMISSIONS)

    def __str__(self):
        return self.name


class Task(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    users = models.ManyToManyField('account.User')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    attach = models.ManyToManyField('TaskFile')
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
    timeleft = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"#{self.group_id} - {self.title[:30]}"

class TaskFile(models.Model):
    file = models.FileField()




