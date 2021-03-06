# Generated by Django 4.0.2 on 2022-03-05 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_alter_booking_backline_provided_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='related_invitation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='related_booking', to='bookings.invitation'),
        ),
    ]
