# Generated by Django 4.1.7 on 2023-03-28 04:51

import core.validators.decorators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_group_id_alter_taskfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(default='Default', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskfile',
            name='file',
            field=models.FileField(upload_to=core.validators.decorators.validator_file_format),
        ),
    ]