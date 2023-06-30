# Generated by Django 4.1.7 on 2023-06-30 03:50

import core.validators.decorators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to=core.validators.decorators.validator_image_format),
        ),
    ]