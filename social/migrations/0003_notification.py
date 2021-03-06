# Generated by Django 4.0.2 on 2022-03-06 16:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0011_remove_booking_country_remove_booking_town_or_city'),
        ('profiles', '0012_alter_audiofile_file'),
        ('social', '0002_message_is_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(4)])),
                ('notification_date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('notification_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_received', to='profiles.userprofile')),
                ('notification_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_sent', to='profiles.userprofile')),
                ('related_booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_notifications', to='bookings.booking')),
                ('related_invitation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitation_notifications', to='bookings.invitation')),
            ],
        ),
    ]
