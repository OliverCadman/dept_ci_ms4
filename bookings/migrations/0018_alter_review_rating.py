# Generated by Django 4.0.2 on 2022-03-23 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0017_alter_booking_related_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
