# Generated by Django 4.0.2 on 2022-02-18 14:36

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0005_alter_audiofile_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitation_number', models.CharField(editable=False, max_length=50)),
                ('event_name', models.CharField(max_length=150, null=True)),
                ('event_city', models.CharField(max_length=100)),
                ('event_country', django_countries.fields.CountryField(max_length=2)),
                ('event_datetime', models.DateTimeField()),
                ('date_of_invitation', models.DateField(auto_now_add=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('invite_receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invitations_received', to='profiles.userprofile')),
                ('invite_sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invitations_sent', to='profiles.userprofile')),
            ],
        ),
    ]