# Generated by Django 4.0.2 on 2022-03-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_sheetmusic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='backline_provided',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='travel_provided',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
