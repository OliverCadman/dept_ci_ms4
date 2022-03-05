from distutils.command.upload import upload
from django.db import models
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save

from profiles.models import UserProfile
import uuid

import datetime


class Invitation(models.Model):
    invitation_number = models.CharField(max_length=50, null=False, editable=False)
    invite_sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                      related_name="invitations_sent", null=True)
    invite_receiver = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        related_name="invitations_received", null=True)
    event_name = models.CharField(max_length=150, null=True)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    event_city = models.CharField(max_length=100)
    event_country = CountryField()
    event_datetime = models.DateTimeField()
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    date_of_invitation = models.DateField(auto_now_add=True)
    additional_info = models.TextField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False, null=True)

    def generate_invitation_number(self):
        """
        Generate random UUID string to represent invitation
        """
        return uuid.uuid4().hex.upper()


    def save(self, *args, **kwargs):
        if not self.invitation_number:
            self.invitation_number = self.generate_invitation_number()
           
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invitation_number


class Booking(models.Model):
    related_invitation = models.OneToOneField(Invitation, on_delete=models.CASCADE,
                                              related_name="related_booking")
    venue_name = models.CharField(max_length=100, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    travel_provided = models.BooleanField(default=False, null=True)
    travel_info = models.TextField(null=True, blank=True)
    backline_provided = models.BooleanField(default=False, null=True)
    backline_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Booking {self.related_invitation.invitation_number}"


class SheetMusic(models.Model):
    related_booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    file_url = models.FileField(upload_to="sheet_music")

    def __str__(self):
        return self.file_url


@receiver(post_save, sender=Invitation)
def create_booking(sender, instance, created, *args, **kwargs):
    if not created:
        invitation = instance
        if invitation.is_accepted == True:
            Booking.objects.create(related_invitation=invitation)
