# Generated by Django 4.0.2 on 2022-03-12 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_remove_job_backline_info_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='image',
            field=models.ImageField(null=True, upload_to='job_images'),
        ),
    ]
