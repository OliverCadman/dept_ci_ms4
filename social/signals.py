from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save

from bookings.models import Invitation
from .models import Notification, Booking


@receiver(post_save, sender=Invitation)
def send_notification_on_invite_sent(sender, instance, **kwargs):
    """
    Sends a user a notification when another user has
    sent an invitation.
    """
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
def send_notification_on_invite_accepted(sender, instance,
                                         created, **kwargs):
    """
    Sends a user a notification once a sent
    invitation has been accepted.
    """
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
def send_notification_on_booking_details_sent(sender, instance,
                                              created, **kwargs):
    """
    Sends a notification once bookings details
    for an accepted invitation have been sent.
    """
    if not created:
        booking = instance
        if booking.booking_details_sent:
            if booking.related_invitation:
                notification_sender = (
                    booking.related_invitation.invite_sender)
                notification_receiver = (
                    booking.related_invitation.invite_receiver)
            else:
                notification_sender = (
                    booking.related_job.job_poster)
                notification_receiver = (
                    booking.related_job.confirmed_member)

            Notification.objects.create(
                notification_sender=notification_sender,
                notification_receiver=notification_receiver,
                notification_type=4,
                related_booking=booking
            )
        else:
            return
