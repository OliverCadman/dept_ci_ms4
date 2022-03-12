# Generated by Django 4.0.2 on 2022-03-12 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_alter_genre_genre_name_and_more'),
        ('jobs', '0003_job_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='job_images'),
        ),
        migrations.AlterField(
            model_name='job',
            name='interested_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs', to='profiles.userprofile'),
        ),
    ]
