from django.db import models

from profiles.models import UserProfile
from bookings.models import Invitation


class Message(models.Model):

    message_sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    message_receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    invitation_id = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True, related_name="invitation_messages")
    date_of_message = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=400)

    def __str__(self):
        return f"Message from {self.message_sender} to {self.message_receiver}"

