import email
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import ImageField
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import email_confirmed

import os

import datetime


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

    instrument_name = models.CharField(max_length=50, unique=True,
                                       choices=INSTRUMENTS, null=True, blank=True)

    def __str__(self):
        return self.instrument_name



class Genre(models.Model):

    POP = "Pop"
    ROCK = "Rock"
    JAZZ = "Jazz"
    CLASSICAL = "Classical"
    FUNK = "Funk"
    SOUL = "Soul"
    RNB = "RnB"
    PUNK = "Punk"
    LATIN = "Latin"
    BOSSA_NOVA = "Bossa Nova"
    HIP_HOP = "Hip Hop"
    METAL = "Metal"
    PROG_ROCK = "Prog Rock"
    EXPERIMENTAL = "Experimental"
    AMBIENT = "Ambient"
    CLUB_MUSIC = "Club Music"
    HOUSE = "House"

    GENRES = [
        (POP, "pop"),
        (ROCK, "rock"),
        (JAZZ, "jazz"),
        (CLASSICAL, "classical"),
        (FUNK, "funk"),
        (SOUL, "soul"),
        (RNB, "rnb"),
        (PUNK, "punk"),
        (LATIN, "latin"),
        (BOSSA_NOVA, "bossa_nova"),
        (HIP_HOP, "hip_hop"),
        (METAL, "metal"),
        (PROG_ROCK, "prog_rock"),
        (EXPERIMENTAL, "experimental"),
        (AMBIENT, "ambient"),
        (CLUB_MUSIC, "club_music"),
        (HOUSE, "house")
    ]

    genre_name = models.CharField(max_length=50, choices=GENRES, 
                                  null=True, blank=True, unique=True)

    def __str__(self):
        return self.genre_name




class UserProfile(models.Model):
 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label="Country", null=True, blank=True)
    profile_image = models.ImageField(upload_to="uploads", null=True, blank=True)
    instruments_played = models.ManyToManyField(Instrument)
    genres = models.ManyToManyField(Genre)
    user_info = models.TextField(null=True, blank=True)
    subscription_chosen = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    


class Equipment(models.Model):
    """
    Database model to display a list of equipment 
    attributed to a particular user.
    """

    class Meta:
        verbose_name_plural = "Equipment"

    equipment_name = models.CharField(max_length=300)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     null=True, blank=True,
                                     related_name="equipment")

    def __str__(self):
        return self.equipment_name


class AudioFile(models.Model):

    file = models.FileField(upload_to="audio")
    file_name = models.CharField(max_length=100, null=True, blank=True)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="users_tracks")

    def get_filename(self, file_path):
        """
        Returns the filename of the audio tracks a user uploads,
        to be used to represent the name each track in the user profile's 
        music player.
        """
        file_url = file_path.url
        file_name = file_url.split("/")[-1]
        self.file_name = file_name

        return self.file_name

    
    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = self.get_filename(self.file)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.file.name




class UnavailableDate(models.Model):

    date = models.DateField(auto_now=False, null=True)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="unavailable_user")

    def __str__(self):

        return str(self.date)


@receiver(post_save, sender=User)
def create_or_update_user(sender, instance, created, **kwargs):
    """
    Create a User Profile when a user registers,
    or update the profile if it's already been created.
    """
    if created:
        UserProfile.objects.create(user=instance)
        print(UserProfile.objects.get(user=instance))
    
    # Otherwise, save the profile.
    instance.userprofile.save()




    


    


