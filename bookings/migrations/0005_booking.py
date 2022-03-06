# Generated by Django 4.0.2 on 2022-03-02 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_invitation_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel_provided', models.BooleanField(default=False)),
                ('travel_info', models.TextField(blank=True, null=True)),
                ('backline_provided', models.BooleanField(default=False)),
                ('backline_info', models.TextField(blank=True, null=True)),
                ('related_invitation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bookings.invitation')),
            ],
        ),
    ]