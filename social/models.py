from django.db import models
from django.core.validators import MaxValueValidator

from profiles.models import UserProfile
from bookings.models import Invitation, Booking



class Message(models.Model):

    message_sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    message_receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    invitation_id = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True, related_name="invitation_messages")
    date_of_message = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message = models.TextField(max_length=400)

    def __str__(self):
        return f"Message from {self.message_sender} to {self.message_receiver}"


class Notification(models.Model):
    """
    Model to represent a notification.

    Fields:

    1. Notification Sender (FK) - The user sending the notification
    2. Notification Receiver (FK) -  The user receiving the notification
    3. Notification Type (SmallInt) - Numbers ranging from 1 - 4:
        1. An invitation has been sent.
        2. An invitation has been accepted.
        3. An invitation has been declined.
        4. A user has sent booking details.
        5. A user has received a message.
        6. A user has received a review.
    
    
    4. Related invitation (FK) - The invitation related to the notification
    5. Related Booking (FK) - The booking related to the notification.
    6. Notification Date - Auto-added when notification is created.
    7. Is Read (Bool) - Boolean Value representing notification has been read.
    """

    notification_sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                            related_name="notifications_sent")
    notification_receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                              related_name="notifications_received")
    notification_type = models.SmallIntegerField(validators=[MaxValueValidator(6)])

    related_invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True,
                                           blank=True, related_name="invitation_notifications")
    
    related_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True,
                                        blank=True, related_name="booking_notifications")
    
    notification_date = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return (f"Notification from {self.notification_sender}\
                to {self.notification_receiver}")


