from django.db import models
from django_countries.fields import CountryField
from profiles.models import UserProfile
import uuid


class Invitation(models.Model):
    invitation_number = models.CharField(max_length=50, null=False, editable=False)
    invite_sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                      related_name="invitations_sent", null=True)
    invite_receiver = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        related_name="invitations_received", null=True)
    event_name = models.CharField(max_length=150, null=True)
    event_city = models.CharField(max_length=100)
    event_country = CountryField()
    event_datetime = models.DateTimeField()
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
            print("Invitation Number:")
            print(self.invitation_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invitation_number