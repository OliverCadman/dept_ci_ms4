from django.db import models
from django.core.validators import MaxValueValidator

from profiles.models import UserProfile
from bookings.models import Invitation, Booking
from jobs.models import Job


class Message(models.Model):
    """
    Message Model
    -------------------

    A model to represent a message sent between users of platform.

    Attributes:
        message_sender (FK): A many-to-one field related to
                             user sending a message.

        message_receiver (FK): A many-to-one field related to
                               user received a message.

        invitation_id (FK): A many-to-one field related to
                            an ongoing invitation.

        related_job (FK): A many-to-one field related to an
                          ongoing job.

        date_of_message (DateTimeField): The date a message was sent.

        is_read (Bool) - A True/False value indicating whether a
                         message has been read.

        message (TextField) - A field to hold message contents.

    Methods:
        __str__(): A string representation of a Message object.
    """

    message_sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                       related_name="sent_messages")
    message_receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                         related_name="received_messages")
    invitation_id = models.ForeignKey(Invitation, on_delete=models.CASCADE,
                                      null=True,
                                      related_name="invitation_messages")
    related_job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True,
                                    blank=True,
                                    related_name="job_messages")
    date_of_message = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message = models.TextField(max_length=400)

    def __str__(self):
        """
        Return a string representation of a message object.
        """
        return (
            f"Message from {self.message_sender} to {self.message_receiver}")


class Notification(models.Model):
    """
    Model to represent a notification.

    Fields:

    1. Notification Sender (FK) - The user sending the notification
    2. Notification Receiver (FK) -  The user receiving the notification
    3. Notification Type (SmallInt) - Numbers ranging from 1 - 7:
        1. An invitation has been sent/a job offer has been sent.
        2. An invitation/job offer has been accepted.
        3. An invitation has been declined.
        4. A user has sent booking details.
        5. A user has received a message.
        6. A user has received a review.
        7. A sent invitation has been deleted.


    4. Related Invitation (FK) - The invitation related to the notification
                                 (nullable)
    5. Related Booking (FK) - The booking related to the notification.
                              (nullable)
    6. Related Job (FK) - The job related to the invitation (nullable).
    7. Declined Invitation (CharField) - Contains the name of a declined
                                         invitation, to preserve the value
                                         once the object is deleted.
    8. Notification Date - Auto-added when notification is created.
    9. Is Read (Bool) - Boolean Value representing notification has been read.

    Methods:

    __str__(): A string representation of a Notification object.
    """

    notification_sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name="notifications_sent")

    notification_receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name="notifications_received")

    notification_type = models.SmallIntegerField(
        validators=[MaxValueValidator(7)])

    related_invitation = models.ForeignKey(
        Invitation, on_delete=models.CASCADE,
        null=True, blank=True, related_name="invitation_notifications")

    related_booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, null=True,
        blank=True, related_name="booking_notifications")

    related_job = models.ForeignKey(
        Job, on_delete=models.CASCADE, null=True,
        blank=True, related_name="job_notifications")

    declined_invitation = models.CharField(
        max_length=150, null=True, blank=True)

    notification_date = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        """
        Return a string representation of a notification object.
        """
        return (
            f"Notification from {self.notification_sender}"
            f" to {self.notification_receiver}")
