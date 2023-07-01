# Generated by Django 4.1.7 on 2023-07-01 03:38

import core.validators.decorators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to=core.validators.decorators.validator_image_format),
        ),
    ]
