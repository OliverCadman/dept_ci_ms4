# Generated by Django 4.0.2 on 2022-03-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_alter_genre_genre_name_and_more'),
        ('jobs', '0004_alter_job_image_alter_job_interested_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='instrument_required',
            field=models.ManyToManyField(to='profiles.Instrument'),
        ),
    ]
