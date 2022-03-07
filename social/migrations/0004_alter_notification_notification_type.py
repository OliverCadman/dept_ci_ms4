# Generated by Django 4.0.2 on 2022-03-06 16:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]