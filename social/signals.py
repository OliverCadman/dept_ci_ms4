from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save


from bookings.models import Invitation
from .models import Notification, Booking


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

@receiver(post_save, sender=Invitation)
def send_notification_on_invite_sent(sender, instance, **kwargs):
    invitation = instance

    if not invitation.is_accepted:
        notification_sender = invitation.invite_sender
        notification_receiver = invitation.invite_receiver

        Notification.objects.create(
            notification_sender=notification_sender,
            notification_receiver=notification_receiver,
            notification_type=1,
            related_invitation=invitation
        )


@receiver(post_save, sender=Invitation)
def send_notification_on_invite_accepted(
    sender, instance, created, **kwargs):
    if not created:
        invitation = instance
        notification_sender = invitation.invite_receiver
        notification_receiver = invitation.invite_sender
        if invitation.is_accepted:
            Notification.objects.create(
                notification_sender=notification_sender,
                notification_receiver=notification_receiver,
                notification_type=2,
                related_invitation=invitation
            )

@receiver(post_save, sender=Booking)
def send_notification_on_booking_details_sent(
    sender, instance, created, **kwargs):
    if not created:
        booking = instance
        notification_sender = booking.related_invitation.invite_sender
        notification_receiver = booking.related_invitation.invite_receiver

        Notification.objects.create(
            notification_sender=notification_sender,
            notification_receiver=notification_receiver,
            notification_type=4,
            related_booking=booking
        )

