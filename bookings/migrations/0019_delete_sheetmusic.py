# Generated by Django 4.0.2 on 2022-03-28 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0018_alter_review_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SheetMusic',
        ),
    ]