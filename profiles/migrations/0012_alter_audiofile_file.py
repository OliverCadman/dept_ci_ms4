# Generated by Django 4.0.2 on 2022-03-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alter_audiofile_related_booking_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='file',
            field=models.FileField(blank=True, upload_to='audio'),
        ),
    ]
