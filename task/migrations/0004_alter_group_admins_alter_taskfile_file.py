# Generated by Django 4.1.7 on 2023-03-28 05:14

import core.validators.decorators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_group_title_alter_taskfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(blank=True, to='task.groupadmin'),
        ),
        migrations.AlterField(
            model_name='taskfile',
            name='file',
            field=models.FileField(upload_to=core.validators.decorators.validator_file_format),
        ),
    ]