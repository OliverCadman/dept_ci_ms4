# Generated by Django 4.0.2 on 2022-03-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_alter_genre_genre_name_and_more'),
        ('jobs', '0005_job_instrument_required'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='interested_member',
        ),
        migrations.AddField(
            model_name='job',
            name='interested_member',
            field=models.ManyToManyField(to='profiles.UserProfile'),
        ),
    ]
