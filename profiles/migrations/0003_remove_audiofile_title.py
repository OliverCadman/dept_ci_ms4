# Generated by Django 4.0.2 on 2022-02-11 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_unavailabledate_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofile',
            name='title',
        ),
    ]
