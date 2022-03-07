from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.shortcuts import get_object_or_404

from bookings.models import Invitation
from profiles.models import UserProfile
from .models import Notification


@receiver(pre_delete, sender=Invitation)
def send_notification_on_decline(sender, instance, **kwargs):
    invitation = instance

    invite_receiver = invitation.invite_receiver
    declined_invitation = invitation.event_name

    Notification.objects.create(
        notification_sender=invite_receiver,
        notification_receiver=invitation.invite_sender,
        notification_type=3,
        declined_invitation=declined_invitation
    )