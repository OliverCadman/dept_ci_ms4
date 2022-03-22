from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth import get_user_model

from profiles.models import UserProfile
from bookings.models import Invitation, Booking
from jobs.models import Job
from social.models import Message, Notification

class TestSocialModels(TestCase):
    """
    Unit Test - Social Model

    Tests Notification and Message Object creation
    and string methods.
    """
    def setUp(self):
        """
        Create two users with user profiles.
        """
        user_model = get_user_model()

        # User 1
        username_1 = "test_user_1"
        password_1 = "test_password_1"
        email_1 = "test_email1"

        self.user_1 = user_model.objects.create_user(
            username=username_1,
            password=password_1,
            email=email_1
        )

        # User 2
        username_2 = "test_user_2"
        password_2 = "test_password_2"
        email_2 = "test_email_2"

        self.user_2 = user_model.objects.create_user(
            username=username_2,
            password=password_2,
            email=email_2
        )

        self.user_profile_1 = get_object_or_404(
            UserProfile, user=self.user_1)

        self.user_profile_2 = get_object_or_404(
            UserProfile, user=self.user_2)

    def test_message_creation_and_string_method(self):
        """
        Create a Message object then retrieve it, and
        confirm that the two message objects are equal.

        Confirm that the Message object returns the
        correct string representation.
        """
        test_message = Message.objects.create(
            message_sender=self.user_profile_1,
            message_receiver=self.user_profile_2,
            message="test_message"
        )

        control_message = Message.objects.get(pk=test_message.pk)
        self.assertEqual(test_message, control_message)

        message_str = f"Message from {self.user_profile_1} to {self.user_profile_2}"
        self.assertEqual(str(test_message), message_str)

    def test_notification_creation_and_string_method(self):
        """
        Create a Notification object then retrieve it, and
        confirm that the two notification objects are equal.

        Confirm that the notification object returns the
        correct string representation.
        """
        test_notification = Notification.objects.create(
            notification_sender=self.user_profile_1,
            notification_receiver=self.user_profile_2,
            notification_type=3
        )

        control_notification = Notification.objects.get(
            pk=test_notification.pk)
        self.assertEqual(test_notification, control_notification)

        notification_str = (
            f"Notification from {self.user_profile_1} to {self.user_profile_2}")
        self.assertEqual(str(test_notification), notification_str)

