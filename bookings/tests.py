from re import S
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .forms import InvitationForm, BookingForm
from .models import Invitation

from profiles.models import UserProfile

import datetime

# Create your tests here.
class TestBookingForms(TestCase):
    """
    Test Validation of Invitation and Booking Forms
    """

    def setUp(self):
        """
        Create two profiles:

        - One for invite sender
        - One for invite receiver
        
        """
        sender_username = "test_sender"
        sender_password = "abc123"
        user_model = get_user_model()
        self.invite_sender = user_model.objects.create_user(
            username=sender_username,
            password=sender_password
        )
        self.sender_profile = UserProfile.objects.get(user__username=self.invite_sender)

        receiver_username = "test_receiver"
        receiver_password = "abc123"
        self.invite_receiver = user_model.objects.create_user(
            username=receiver_username,
            password=receiver_password
        )
        self.receiver_profile = UserProfile.objects.get(user__username=self.invite_receiver)

        self.client = Client()
        

    def test_invitation_form_valid_and_redirect_success(self):
       """
       Confirm Invitation form validates correctly and redirects
       to invite receiver's profile upon submission.
       """
       form = InvitationForm(data={
           "event_name": "test_event",
           "artist_name": "test_artist",
           "event_city": "test_city",
           "event_country": "GB",
           "event_datetime": timezone.now(),
           "fee": 150,
           "date_of_invitation": datetime.date.today(),
           "additional_info": "test_additional_info",
           "invite_sender": self.sender_profile,
           "invite_receiver": self.receiver_profile

       })
       
       self.assertTrue(form.is_valid())
       
       response = self.client.get(reverse("profile", args=[self.receiver_profile.user]))
       self.assertEquals(response.status_code, 200)

    def test_invitation_form_without_data(self):
        empty_invitation_form = InvitationForm(data={})

        self.assertFalse(empty_invitation_form.is_valid())

    
    def test_booking_form_valid(self):
        """
        Confirm Booking Form validates correctly.
        """
        invitation = Invitation.objects.create(
            event_name="test_event",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime = timezone.now(),
            fee=150,
            date_of_invitation=datetime.date.today(),
            additional_info="test_additional_info",
            invite_sender=self.sender_profile,
            invite_receiver=self.receiver_profile
        )

        booking_form = BookingForm(data={
            "related_invitation": invitation.pk,
            "travel_provided": True,
            "travel_info": "test_travel_info",
            "backline_provided":  True,
            "backline_info": "test_backline_info"
        })

        self.assertTrue(booking_form.is_valid())
        



    


