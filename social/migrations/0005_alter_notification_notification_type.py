# Generated by Django 4.0.2 on 2022-03-06 16:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(6)]),
        ),
    ]
