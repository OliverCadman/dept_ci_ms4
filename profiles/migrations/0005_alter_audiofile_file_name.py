# Generated by Django 4.0.2 on 2022-02-14 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_audiofile_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='file_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
