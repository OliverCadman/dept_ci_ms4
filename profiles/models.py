import email
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import email_confirmed

import datetime


class UserProfile(models.Model):
 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label="Country", null=True, blank=True)
    subscription_chosen = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class AudioFile(models.Model):

    file = models.FileField(upload_to="audio")
    title = models.CharField(max_length=100)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="users_tracks")

    def __str__(self):
        return self.title


class Instrument(models.Model):

    # Assigning first value in 'choices' tuple to avoid
    # errors and seperate logic.
    VOCALS = "Vocals"
    GUITAR = "Guitar"
    BASS_GUITAR = "Bass Guitar"
    KEYBOARD = "Keyboard"
    PIANO = "Piano"
    DRUMS = "Drums"
    PERC = "Percussion"
    TRUMPET = "Trumpet"
    TENOR_TROMB = "Tenor Trombone"
    BASS_TROMB = "Bass Trombone"
    SOUSAPHONE = "Sousaphone"
    TENOR_SAX = "Tenor Saxophone"
    ALTO_SAX = "Alto Saxphone"
    BARITONE_SAX = "Baritone Saxophone"
    FLUTE = "Flute"
    CLARINET = "Clarinet"
    ACCORDION = "Accordion"
    VIOLIN = "Violin"
    CELLO = "Cello"
    DOUBLE_BASS = "Double Bass"
    VIOLA = "Viola"
    VIBRAPHONE = "Vibraphone"
    HARMONICA = "Harmonica"

    # Define the choices available to the user when selecting their instruments.
    # Passed as 'choices' argument in CharField.
    INSTRUMENTS = [
        (VOCALS, "vocals"),
        (GUITAR, "guitar"),
        (BASS_GUITAR, "bass guitar"),
        (KEYBOARD, "keyboard"),
        (PIANO, "piano"),
        (DRUMS, "drums"),
        (PERC, "percussion"),
        (TRUMPET, "trumpet"),
        (TENOR_TROMB, "tenor trombone"),
        (BASS_TROMB, "bass_trombone"),
        (SOUSAPHONE, "sousaphone"),
        (ALTO_SAX, "alto saxophone"),
        (TENOR_SAX, "tenor saxophone"),
        (BARITONE_SAX, "baritone saxophone"),
        (FLUTE, "flute"),
        (CLARINET, "clarinet"),
        (ACCORDION, "accordion"),
        (VIOLIN, "violin"),
        (VIOLA, "viola"),
        (CELLO, "cello"),
        (DOUBLE_BASS, "double bass"),
        (HARMONICA, "harmonica"),
        (VIBRAPHONE, "vibraphone")
    ]

    instrument_name = models.CharField(max_length=50,
                                       choices=INSTRUMENTS, default="")
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="related_user")

    def __str__(self):
        return self.instrument_name



class UnavailableDate(models.Model):

    date = models.DateTimeField(auto_now=False, null=True)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="unavailable_user")

    def __str__(self):

        return self.date


# @receiver(post_save, sender=User)
# def create_or_update_user(sender, instance, created, **kwargs):
#     """
#     Create a User Profile when a user registers,
#     or update the profile if it's already been created.
#     """
#     if created:
#         UserProfile.objects.create(user=instance)
#         print(UserProfile.objects.get(user=instance))
    
#     # Otherwise, save the profile.
#     instance.userprofile.save()

@receiver(email_confirmed)
def create_profile(request, email_address, **kwargs):
    """ Create a Profile when a user signs up """
    user_model = get_user_model()
    user = user_model.objects.get(emailaddress=email_address)
    UserProfile.objects.create(user=user)



    


    


