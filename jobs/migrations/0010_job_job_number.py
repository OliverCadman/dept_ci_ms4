# Generated by Django 4.0.2 on 2022-03-24 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_remove_job_instrument_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
