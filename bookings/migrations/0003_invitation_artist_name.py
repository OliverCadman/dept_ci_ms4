# Generated by Django 4.0.2 on 2022-02-18 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_invitation_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='artist_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]