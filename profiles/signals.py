from bookings.models import Invitation
from .models import UserProfile

from django.shortcuts import get_object_or_404
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

"""
Profile App - Signals
-------------------------

Provide functionality to update UserProfile invitation
count when an Invitation object is made, with the Userprofile
as the invite receiver.
"""


@receiver(post_save, sender=Invitation)
def increment_invitation_count(sender, instance, created, **kwargs):
    """
    Increments a UserProfile's invitation count upon
    each invitation they received.
    """
    if created:
        invite_receiver = instance.invite_receiver
        invited_receiver_profile = get_object_or_404(
            UserProfile, user__username=invite_receiver)
        invited_receiver_profile.invitation_count += 1
        invited_receiver_profile.save()
    else:
        return None
