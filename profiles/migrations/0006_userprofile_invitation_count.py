# Generated by Django 4.0.2 on 2022-02-22 10:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_audiofile_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='invitation_count',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
