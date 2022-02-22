from bookings.models import Invitation
from .models import UserProfile

from django.shortcuts import get_object_or_404
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Invitation)
def increment_invitation_count(sender, instance, created, **kwargs):
    if created:
        invite_receiver = instance.invite_receiver
        invited_receiver_profile = get_object_or_404(UserProfile, user__username=invite_receiver)
        invited_receiver_profile.invitation_count += 1
        invited_receiver_profile.save()
        
   
    
