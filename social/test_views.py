from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from test_helpers import (create_test_user, create_test_invitation,
                          create_test_job)

from profiles.models import UserProfile
from bookings.models import Invitation, Booking
from jobs.models import Job
from social.functions import get_referral_path, reverse_querystring
from social.models import Notification


class TestSocialViews(TestCase):
    """
    Unit Testing for Views related to the Social App

    Unit Tests concern Notifications and Messages.
    """

    def setUp(self):
        """
        Set up test users and log first test
        user in.
        """

        # Test User 1
        username = "test"
        password = "test"
        email = "test@test.com"

        self.test_user = create_test_user(username, password, email)
        self.test_user_profile = get_object_or_404(
            UserProfile, user__username=self.test_user)

        # Subscribe and add paid status to User 1
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.is_paid = True
        self.test_user_profile.save()

        # Test User 2
        username2 = "test2"
        password2 = "test2"
        email2 = "test2@test.com"

        self.test_user2 = create_test_user(username2, password2, email2)
        self.test_user_profile2 = get_object_or_404(
            UserProfile, user__username=self.test_user2)

        # Subscribe and add paid status to User 2
        self.test_user_profile2.subscription_chosen = True
        self.test_user_profile.is_paid = True
        self.test_user_profile2.save()

        # Instantiate the client
        self.client = Client()
        logged_in = self.client.login(username=username, password=password)

        self.assertTrue(logged_in)

    def test_send_message_tier_one_POST(self):
        """
        Test View to Send Message for Tier One invitations.

        Confirm that the view returns a successful redirect
        response, and redirects the message sender back
        to their dashboard, with the appropriate success message.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile2
        )

        # Referal URL required to determine whether the message concerns
        # a Tier One Invitation or a Tier Two Job
        referal_url = "http://127.0.0.1:8000" + reverse_querystring(
                                          "dashboard",
                                          args=[self.test_user_profile.slug],
                                          query_kwargs={
                                              "page": "jobs",
                                              "section": "tier_one",
                                              "subsection": "invites_sent",
                                              "filter": "all"
                                          })
        # Prepare message POST request
        message_post = {
            "message": "test_message"
        }

        # Determine successful response
        response = self.client.post(
            reverse("send_message",
                    args=[self.test_user_profile2, test_invitation.pk]),
            message_post, HTTP_REFERER=referal_url, follow=True)

        messages = list(get_messages(response.wsgi_request))
        success_msg = "Message sent to test2"

        success_redirect_url = reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs"
            })

        # Successful Redirect
        self.assertRedirects(response, success_redirect_url, status_code=302,
                             target_status_code=200)

        # Appropriate success message
        self.assertEqual(str(messages[0]), success_msg)

    def test_send_invalid_tier_one_message_POST(self):
        """
        Test View to Send Message for Tier One invitations.

        Confirm that the view returns a successful redirect
        response, and redirects the message sender back
        to their dashboard, with the appropriate success message.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile2
        )

        # Referal URL required to determine whether the message concerns
        # a Tier One Invitation or a Tier Two Job
        referal_url = "http://127.0.0.1:8000" + reverse_querystring(
                                          "dashboard",
                                          args=[self.test_user_profile.slug],
                                          query_kwargs={
                                              "page": "jobs",
                                              "section": "tier_one",
                                              "subsection": "invites_sent",
                                              "filter": "all"
                                          })
        # Prepare message POST request
        message_post = {
            "message": ""
        }

        # Determine successful response
        response = self.client.post(
            reverse("send_message",
                    args=[self.test_user_profile2, test_invitation.pk]),
            message_post, HTTP_REFERER=referal_url, follow=True)

        messages = list(get_messages(response.wsgi_request))
        error_msg = ("Sorry, message not sent."
                     " Please make sure your message is valid.")

        success_redirect_url = reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs"
            })

        # Successful Redirect
        self.assertRedirects(response, success_redirect_url,
                             status_code=302, target_status_code=200)

        # Appropriate success message
        self.assertEqual(str(messages[0]), error_msg)

    def test_send_message_tier_two_POST(self):
        """
        Test View to Send Message for Tier One invitations.

        Confirm that the view returns a successful redirect
        response, and redirects the message sender back
        to their dashboard, with the appropriate success message.
        """

        test_job = create_test_job(
            self.test_user_profile
        )

        test_job_object = get_object_or_404(Job, pk=test_job.pk)
        test_job_object.confirmed_member = self.test_user_profile2
        test_job_object.is_taken = True
        test_job_object.save()

        Booking.objects.create(
            related_job=test_job
        )

        # Referal URL required to determine whether the message concerns
        # a Tier One Invitation or a Tier Two Job
        referal_url = "http://127.0.0.1:8000" + reverse_querystring(
                                          "dashboard",
                                          args=[self.test_user_profile.slug],
                                          query_kwargs={
                                              "page": "jobs",
                                              "section": "tier_two",
                                              "subsection": "posted_jobs",
                                              "filter": "all"
                                          })
        # Prepare message POST request
        message_post = {
            "message": "test_message"
        }

        # Determine successful response
        response = self.client.post(
            reverse("send_message",
                    args=[self.test_user_profile2, test_job.pk]),
            message_post, HTTP_REFERER=referal_url, follow=True)

        messages = list(get_messages(response.wsgi_request))
        success_msg = "Message sent to test2"

        success_redirect_url = reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs"
            })

        # Successful Redirect
        self.assertRedirects(response, success_redirect_url, status_code=302,
                             target_status_code=200)

        # Appropriate success message
        self.assertEqual(str(messages[0]), success_msg)

    def test_invitation_received_notification_view(self):
        """
        Test the GET method of the view which handles
        the event that a user receives an invitation.

        Confirm that the appropriate Notification object's
        "is_read" status is set to "True", and the user is
        redirected to their Dashboard with a successful response.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile2,
            self.test_user_profile
        )

        test_notification = Notification.objects.create(
            notification_sender=self.test_user_profile2,
            notification_receiver=self.test_user_profile,
            notification_type=1,
            related_invitation=test_invitation
        )

        # Confirm the User is taken to this URL upon clicking
        # notification.
        target_success_url = reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_one",
                "subsection": "invites_received",
                "filter": test_invitation.pk
            }
        )

        response = self.client.get(
            reverse("invite_received_notification",
                    args=[test_notification.pk, test_invitation.pk]))

        self.assertRedirects(response, target_success_url, status_code=302,
                             target_status_code=200)

    def test_invite_accepted_notification_view(self):
        """
        Test the GET method of the view which handles
        the event that a user accepts an invitation.

        Confirm that the appropriate Notification object's
        "is_read" status is set to "True", and the user is
        redirected to the Booking form with a successful response.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile2
        )

        test_invitation_object = get_object_or_404(
            Invitation, pk=test_invitation.pk)

        # Set the "is accepted" status of Invitation object to
        # True" to create booking object.
        # This is needed to successfully navigate to redirect URL.
        test_invitation_object.is_accepted = True
        test_invitation_object.save()

        test_notification = Notification.objects.create(
            notification_sender=self.test_user_profile2,
            notification_receiver=self.test_user_profile,
            notification_type=2,
            related_invitation=test_invitation
        )

        # Confirm the User is taken to this URL upon clicking
        # notification.
        target_success_url = reverse("booking_form", args=[test_invitation.pk])

        response = self.client.get(
            reverse("invite_accepted_notification",
                    args=[test_notification.pk, test_invitation.pk]))

        self.assertRedirects(response, target_success_url, status_code=302,
                             target_status_code=200)

    def test_booking_details_sent_notification(self):
        """
        Test the GET method of the view which handles
        the event that a user has received booking details.

        Confirm that the appropriate Notification object's
        "is_read" status is set to "True", and the user is
        redirected to the Booking Detail page with a successful
        response.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile2,
            self.test_user_profile
        )

        test_invitation_object = get_object_or_404(
            Invitation, pk=test_invitation.pk)
        test_invitation_object.is_accepted = True
        test_invitation_object.save()

        test_booking_object = get_object_or_404(
            Booking, related_invitation=test_invitation)
        test_booking_object.booking_details_sent = True
        test_booking_object.save()

        test_notification = Notification.objects.create(
            notification_sender=self.test_user_profile2,
            notification_receiver=self.test_user_profile,
            notification_type=4,
            related_booking=test_booking_object
        )

        # Confirm the User is taken to this URL upon clicking
        # notification.
        target_success_url = reverse(
            "booking_detail", args=[test_booking_object.pk])

        response = self.client.get(
            reverse("booking_details_sent_notification",
                    args=[test_notification.pk, test_booking_object.pk]))

        self.assertRedirects(
            response, target_success_url,
            status_code=302, target_status_code=200)

    def test_remove_notification_GET(self):
        """
        Test the removal of notifications from the
        notification dropdown. Confirm that the
        view returns a successful HTTPResponse.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile2
        )

        test_invitation_object = get_object_or_404(
            Invitation, pk=test_invitation.pk)

        # Set the "is accepted" status of Invitation object to "True"
        # to create  booking object. This is needed to
        # successfully navigate to redirect URL.
        test_invitation_object.is_accepted = True
        test_invitation_object.save()

        test_notification = Notification.objects.create(
            notification_sender=self.test_user_profile2,
            notification_receiver=self.test_user_profile,
            notification_type=2,
            related_invitation=test_invitation
        )

        response = self.client.get(reverse("remove_notification",
                                           args=[test_notification.pk]))

        self.assertEqual(response.status_code, 200)
