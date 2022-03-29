from django.shortcuts import get_object_or_404
from django.test import (TestCase, Client, RequestFactory,
                         override_settings)
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages import get_messages, get_level
from django.test.utils import tag
from django.conf import settings
from unittest import mock

from profiles.models import (UserProfile, AudioFile,
                             UnavailableDate, Instrument, Genre)
from bookings.models import Review, Invitation, Booking
from profiles.views import ProfileView, delete_stripe_customer
from social.functions import reverse_querystring
from social.models import Notification
from jobs.models import Job

from test_helpers import create_test_user, create_test_invitation

import tempfile
import datetime
import stripe

"""
Profile Views - Unit Tests

Test the various GET and POST methods for Profile App Views

Classes:
    TestProfileViewGETMethods

    TestProfileViewPOSTMethods
"""


class TestProfileViewGETMethods(TestCase):

    def setUp(self):
        """
        Create a mock user and retrieve their user
        profile to pass in as args to the URLs.
        """
        username = "test_user"
        password = "abcde12345"
        email = "test@test.com"

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        self.user_profile = get_object_or_404(
            UserProfile, user=self.user)

        # Instantiate a client to mimic a user
        self.client = Client()
        self.client.login(username=username, password=password)

        # Define the URLs to be called
        self.get_users_unavailable_dates_url = reverse(
            "get_users_unavailable_dates", args=[self.user.pk])

        self.get_users_tracks_url = reverse(
            "get_users_tracks", args=[self.user.pk])

        self.profile_url = reverse("profile", args=[self.user])

        self.edit_profile_url = reverse("edit_profile")

        self.upload_audio_url = reverse("upload_audio", args=[self.user])

        self.dashboard_url = reverse(
            "dashboard", args=[self.user_profile.slug])

        self.delete_account_url = reverse(
            "delete_account", args=[self.user_profile.pk])

# -------------------- User Profile ----------------------

    def test_get_users_unavailable_dates_response(self):
        """
        Create an Unavailable Date object, related to
        the user profile created in setUp method.

        Confirm a successful JSONresponse, and that the
        "unavailable_dates" key is in the object, along
        with the correct value.
        """
        unavailable_date = UnavailableDate.objects.create(
            date=timezone.localdate(),
            related_user=self.user_profile
        )

        unavailable_date_list = []

        # Control value
        unavailable_date = str(unavailable_date.date)
        unavailable_date_list.append(unavailable_date)

        # GET Request
        response = self.client.get(self.get_users_unavailable_dates_url)
        json_response = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertTrue("unavailable_dates" in response.json())
        self.assertEquals(json_response["unavailable_dates"],
                          unavailable_date_list)

    def test_get_users_tracks_response(self):
        """
        Test AJAX Handler to confirm the URL returns
        a successful response, and that the "track_list"
        key is in the JSON.
        """
        response = self.client.get(self.get_users_tracks_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("track_list" in response.json())

    def test_profile_response(self):
        """
        Confirm a successful response upon visiting
        a user profile.
        """
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("profiles/profile.html")

    def test_profile_context(self):
        """
        Confirm that all the required keys for
        the profile page are present in the response's context.
        """
        response = self.client.get(self.profile_url)

        self.assertTrue("user" in response.context)
        self.assertTrue("page_name" in response.context)
        self.assertTrue("instrument_list" in response.context)
        self.assertTrue("users_tracks" in response.context)
        self.assertTrue("users_genres" in response.context)
        self.assertTrue("track_filename" in response.context)
        self.assertTrue("username" in response.context)
        self.assertTrue("user_id" in response.context)
        self.assertTrue("invitation_form" in response.context)
        self.assertTrue("review_form" in response.context)
        self.assertTrue("average_rating" in response.context)
        self.assertTrue("num_of_reviews" in response.context)

    # def test_calculate_average_rating_in_profile_view(self):
    #     """
    #     Confirm that the Profile view returns the correct
    #     average rating.
    #     """

    #     # Create second mock user_profile to send a review
    #     # to self.user_profile.
    #     user_model = get_user_model()
    #     test_review_sender = user_model.objects.create_user(
    #         username="review_sender",
    #         password="reviewer_password",
    #         email="reviewer_email"
    #     )

    #     # Get UserProfile for Test Review Sender to related to test Reviews.
    #     test_reviewsender_userprofile = get_object_or_404(
    #         UserProfile, user=test_review_sender)

    #     test_reviewsender_userprofile.first_name = "Test First Name"
    #     test_reviewsender_userprofile.save()

    #     self.user_profile.first_name = "Test First Name"
    #     self.user_profile.save()

    #     # Create three reviews related to second mock user_profile/
    #     Review.objects.bulk_create([
    #         Review(
    #             review_sender=test_reviewsender_userprofile,
    #             review_receiver=self.user_profile,
    #             review_content="test review 1",
    #             review_created=timezone.now(),
    #             rating=3
    #         ),
    #         Review(
    #             review_sender=test_reviewsender_userprofile,
    #             review_receiver=self.user_profile,
    #             review_content="test review 2",
    #             review_created=timezone.now(),
    #             rating=5
    #         ),
    #         Review(
    #             review_sender=test_reviewsender_userprofile,
    #             review_receiver=self.user_profile,
    #             review_content="test review 3",
    #             review_created=timezone.now(),
    #             rating=2
    #         )
    #     ])

    #     # Calculate the rating to use as a control.
    #     control_total_rating = 3 + 5 + 2
    #     control_num_of_reviews = 3
    #     control_average_rating = round(
    #         control_total_rating / control_num_of_reviews)
    #     response = self.client.get(self.profile_url)

    #        Confirm that the average rating in th
    #  response matches the control.
    #     self.assertEqual(
    #         response.context["average_rating"], control_average_rating)

    def test_users_tracks_in_profile_context(self):
        """
        Create a mock audio file related to self.user_profile,
        and confirm that the file object is present in
        self.user_profile's profile.
        """
        file = tempfile.NamedTemporaryFile(suffix=".mp3").name

        audiofile = AudioFile.objects.create(
            file=file,
            related_user=self.user_profile
        )

        response = self.client.get(self.profile_url)
        self.assertEqual(
            response.context["track_filename"], audiofile.file_name)

    # ----------------------- Edit Profile ---------------------

    def test_edit_profile_url_GET(self):
        """
        Confirm that the Edit Profile URL's GET request
        returns a successful response.
        """

        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_upload_audio_GET(self):
        """
        Confirm a successful GET response in upload audio
        AJAX handler, and confirm that the success message
        and form page keys are in the returned JSON object.
        """
        response = self.client.get(self.upload_audio_url)
        self.assertTrue("success_msg" in response.json())
        self.assertTrue("form_page" in response.json())

# ----------------- Dashboard --------------------

    @tag("skip_setup")
    def test_dashboard_redirect_for_unauthorized_user(self):
        """
        Create a mock unauthorized user to act as user trying
        to visit another member's private dashboard.

        Confirm that they are redirected to the appropriate
        page with a success response, if they attempt to visit
        another member's dashboard.
        """

        user_model = get_user_model()

        # Authorized user details
        authorized_username = "authorized"
        authorized_password = "authorized123"
        authorized_email = "authorized@knockyerselfout.com"

        # Unauthorized user details
        unauthorized_username = "unauthorized"
        unauthorized_password = "unauthorized"
        unauthorized_email = "unauthorized@youshouldgetoutrightaway.com"

        # Authorized User Object and Profile
        authorized_user = user_model.objects.create_user(
            username=authorized_username,
            password=authorized_password,
            email=authorized_email
        )

        authorized_userprofile = get_object_or_404(
            UserProfile, user=authorized_user)

        # Unauthorized User Object and Profile
        unauthorized_user = user_model.objects.create_user(
            username=unauthorized_username,
            password=unauthorized_password,
            email=unauthorized_email
        )

        unauthorized_userprofile = get_object_or_404(
            UserProfile, user=unauthorized_user)

        # Log the unauthorized user in
        client = Client()
        logged_in = client.login(
            username=unauthorized_username,
            password=unauthorized_password
        )
        self.assertTrue(logged_in)

        # Attempt to visit authorized user's dashboard.
        response = client.get(reverse(
            "dashboard", args=[authorized_userprofile.slug]),
            follow=True)

        redirect_url = reverse_querystring(
            "dashboard",
            args=[unauthorized_userprofile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_one"
            })

        # Confirm redirect to the url defined above,
        # with the appropriate status codes.
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200)

    def test_dashboard_redirect_if_unpaid_user_visits_tiertwo(self):
        """
        Confirm that an unpaid user is redirected if they attempt
        to access Tier Two content.
        """
        user_profile = self.user_profile
        user_profile.is_paid = False
        user_profile.save()

        tier_two_access_url = reverse_querystring(
                "dashboard",
                args=[user_profile.slug],
                query_kwargs={
                    "page": "jobs",
                    "section": "tier_two"
                })

        redirect_url = reverse_querystring(
                "dashboard",
                args=[user_profile.slug],
                query_kwargs={
                    "page": "jobs",
                    "section": "tier_one"
                })

        response = self.client.get(tier_two_access_url, follow=True)

        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200)

    def test_dashboard_calculate_average_rating(self):
        """
        Confirm the "average_rating" functionality works
        as intended.
        """

        # Create mock review_sender profile
        user_model = get_user_model()
        test_review_sender = user_model.objects.create_user(
            username="review_sender",
            password="reviewer_password",
            email="reviewer_email"
        )

        # Get UserProfile for Test Review Sender to related to test Reviews.
        test_reviewsender_userprofile = get_object_or_404(
            UserProfile, user=test_review_sender)

        # Create three reviews
        Review.objects.bulk_create([
            Review(
                review_sender=test_reviewsender_userprofile,
                review_receiver=self.user_profile,
                review_content="test review 1",
                review_created=timezone.now(),
                rating=3
            ),
            Review(
                review_sender=test_reviewsender_userprofile,
                review_receiver=self.user_profile,
                review_content="test review 2",
                review_created=timezone.now(),
                rating=5
            ),
            Review(
                review_sender=test_reviewsender_userprofile,
                review_receiver=self.user_profile,
                review_content="test review 3",
                review_created=timezone.now(),
                rating=2
            )
        ])

        # Calculate control rating
        control_total_rating = 3 + 5 + 2
        control_num_of_reviews = 3
        control_average_rating = round(
            control_total_rating / control_num_of_reviews)

        # Confirm that the value returned in the response
        # context matches the control.
        response = self.client.get(
            reverse("dashboard", args=[self.user_profile.slug]))
        self.assertEqual(
            response.context["average_rating"], control_average_rating)
        self.assertEqual(
            response.context["num_of_reviews"], control_num_of_reviews)

    def test_queryargs_in_dashboard_URL_query(self):
        """
        Test the various routes the user can take on the
        Dashboard's Job Page and confirm that they return
        a successful response, and that the response's
        context matches the parameters provided in the URL query.

        Structured thus: (Page, Section, Subsection, Filter)
            (Page) - Job Page
                (Section) - Tier One
                   (Subsection) - Invites Received
                            (Filter) - All
                            (Filter) - Pending
                            (Filter) - Accepted
                            (Filter) - Invitation ID
                    (Subsection) - Invites Sent
                            (Filter) - All
                            (Filter) - Pending
                            (Filter) - Accepted
                            (Filter) - Booking ID
                (Section) - Tier Two
                    (Subsection) - Jobs Posted
                            (Filter) - All
                            (Filter) - Pending Offers
                            (Filter) - Confirmed
                    (Subection) - Offers Sent
                            (Filter) - All
                            (Filter) - Pending Confirmation
                            (Filter) - Confirmed
        """

        # Create a mock user to act as invitation/job poster
        # Used in order to create invitation/booking/job object
        # to use it's ID as filter.
        user_model = get_user_model()
        test_poster = user_model.objects.create_user(
            username="invite_poster",
            password="inviter_password",
            email="inviter_email@invite.com"
        )

        # Get UserProfile for Test Invitation/Job Post Sender.
        test_poster_userprofile = get_object_or_404(
            UserProfile, user=test_poster)

        # ----- Tier One ------

        # ----- Invites Received ------

        # --- Filter: All
        dashboard_url_tierone_invites_received_all = (
            reverse_querystring("dashboard", args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_received",
                                    "filter": "all"
                                })
        )

        # Filter: All Response
        response = self.client.get(dashboard_url_tierone_invites_received_all)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_received")
        self.assertTrue(response.context["current_filter"], "all")

        # --- Filter: Pending
        dashboard_url_tierone_invites_received_pending = (
            reverse_querystring("dashboard", args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_received",
                                    "filter": "pending"
                                }))

        # Filter: Pending Response
        response = self.client.get(
            dashboard_url_tierone_invites_received_pending)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_received")
        self.assertTrue(response.context["current_filter"], "pending")

        # Filter: Accepted
        dashboard_url_tierone_invites_received_accepted = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_received",
                                    "filter": "accepted"
                                }))

        # Filter: Accepted Response)
        response = self.client.get(
            dashboard_url_tierone_invites_received_accepted)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_received")
        self.assertTrue(response.context["current_filter"], "accepted")

        # Filter: Invitation ID
        test_invitation = Invitation.objects.create(
            invite_sender=test_poster_userprofile,
            invite_receiver=self.user_profile,
            event_name="test_event",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime=datetime.datetime.now(),
            fee=150.00,
            additional_info="test_additional_info"
        )

        test_invitation.is_accepted = True
        test_invitation.save()

        dashboard_url_tierone_invites_received_invitation_id = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_received",
                                    "filter": test_invitation.pk
                                }))

        # Filter: Invitation ID Response
        response = self.client.get(
            dashboard_url_tierone_invites_received_invitation_id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_received")
        self.assertTrue(response.context["current_filter"], test_invitation.pk)

        # Retrieve test_booking related to invitation to test filter
        # by it's ID.
        test_booking = get_object_or_404(
            Booking, related_invitation=test_invitation)

        # Filter: Booking ID
        dashboard_url_tierone_invites_received_booking_id = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_received",
                                    "filter": test_booking.pk
                                }))

        # Filter: Booking ID Response
        response = self.client.get(
            dashboard_url_tierone_invites_received_booking_id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_received")
        self.assertTrue(response.context["current_filter"], test_booking.pk)

        # -------- Invites Sent --------

        # Filter: All
        dashboard_tierone_url_invites_sent = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_sent",
                                    "filter": "all"
                                }))

        # Filter: All Response
        response = self.client.get(dashboard_tierone_url_invites_sent)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_sent")
        self.assertTrue(response.context["current_filter"], "all")

        # Filter: Pending
        dashboard_url_tierone_invites_sent_pending = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_sent",
                                    "filter": "pending"
                                }))

        # Filter: Pending Response
        response = self.client.get(
            dashboard_url_tierone_invites_sent_pending)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_sent")
        self.assertTrue(response.context["current_filter"], "pending")

        # Filter: Accepted
        dashboard_url_tierone_invites_sent_accepted = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_sent",
                                    "filter": "accepted"
                                }))

        # Filter: Accepted Response
        response = self.client.get(
            dashboard_url_tierone_invites_sent_accepted)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"],
                        "invites_sent")
        self.assertTrue(response.context["current_filter"], "accepted")

        # Filter: Booking ID
        dashboard_url_tierone_invites_sent_bookingID = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_sent",
                                    "filter": "2"
                                }))

        # Filter: BookingID response
        response = self.client.get(
            dashboard_url_tierone_invites_sent_bookingID)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_one")
        self.assertTrue(response.context["current_subsection"], "invites_sent")
        self.assertTrue(response.context["current_filter"], "2")

        # ------------------- Tier Two -----------------------

        # Set "is_paid" status on self.user_profile in order to access content.
        self.user_profile.is_paid = True
        self.user_profile.save()

        # ---------- Posted Jobs -------------

        # Filter: All
        dashboard_url_tier_two_posted_jobs_all = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "posted_jobs",
                                    "filter": "all"
                                }))

        # Filter: All Response
        response = self.client.get(
            dashboard_url_tier_two_posted_jobs_all)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "posted_jobs")
        self.assertTrue(response.context["current_filter"], "all")

        # Filter: Pending
        dashboard_url_tier_two_posted_jobs_pending = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "posted_jobs",
                                    "filter": "pending_offers"
                                }))

        # Filter: Pending Response
        response = self.client.get(
            dashboard_url_tier_two_posted_jobs_pending)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "posted_jobs")
        self.assertTrue(response.context["current_filter"], "pending_offers")

        # Filter: Confirmed
        dashboard_url_tier_two_posted_jobs_accepted = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "posted_jobs",
                                    "filter": "confirmed"
                                }))

        # Filter: Confirmed Response
        response = self.client.get(
            dashboard_url_tier_two_posted_jobs_accepted)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "posted_jobs")
        self.assertTrue(response.context["current_filter"], "confirmed")

        # ---------- Offers Sent ----------

        # Filter: All
        dashboard_url_tier_two_offers_sent_all = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "offers_sent",
                                    "filter": "all"
                                }))

        # Filter: All Response
        response = self.client.get(
            dashboard_url_tier_two_offers_sent_all)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "offers_sent")
        self.assertTrue(response.context["current_filter"], "all")

        # Filter: Pending
        dashboard_url_tier_two_offers_sent_pending_offers = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "offers_sent",
                                    "filter": "pending_offers"
                                }))

        # Filter: Pending Response
        response = self.client.get(
            dashboard_url_tier_two_offers_sent_pending_offers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "offers_sent")
        self.assertTrue(response.context["current_filter"], "pending_offers")

        # Filter: Confirmed
        dashboard_url_tier_two_offers_sent_confirmed = (
            reverse_querystring("dashboard",
                                args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "offers_sent",
                                    "filter": "confirmed"
                                }))

        # Filter: Confirmed Response
        response = self.client.get(
            dashboard_url_tier_two_offers_sent_confirmed)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "offers_sent")
        self.assertTrue(response.context["current_filter"], "confirmed")

        # Filter: Job ID

        # Create Job to use it's ID to filter.
        test_job = Job.objects.create(
            job_poster=test_poster_userprofile,
            job_title="test_job",
            event_name="test_job",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime=datetime.datetime.now(),
            fee=150.00,
            job_description="test_job_description"
        )

        test_job.confirmed_member = self.user_profile
        test_job.save()

        Booking.objects.create(
            related_job=test_job
        )

        test_booking = Booking.objects.get(
            related_job__event_name="test_job"
        )

        test_booking.booking_details_sent = True
        test_booking.save()

        # Filter: Job ID
        dashboard_url_tier_two_offers_sent_job_pk = (
            reverse_querystring("dashboard", args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_two",
                                    "subsection": "offers_sent",
                                    "filter": test_job.pk
                                }))

        response = self.client.get(
            dashboard_url_tier_two_offers_sent_job_pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_page"], "jobs")
        self.assertTrue(response.context["current_section"], "tier_two")
        self.assertTrue(response.context["current_subsection"], "offers_sent")
        self.assertTrue(response.context["current_filter"], test_job.pk)

        # Confirm Invitation is returned when searching by Booking ID

        username = "test"
        password = "test"
        email = "test"

        invite_receiver = create_test_user(username, password, email)
        invite_receiver_profile = get_object_or_404(
            UserProfile, user__username=invite_receiver)

        test_invitation = create_test_invitation(
            self.user_profile, invite_receiver_profile)
        retrieved_invitation = Invitation.objects.get(pk=test_invitation.pk)
        retrieved_invitation.is_accepted = True
        retrieved_invitation.save()

        test_booking = Booking.objects.get(
            related_invitation__pk=test_invitation.pk)

        booking_success_response = self.client.get(
            reverse("booking_detail", args=[test_booking.pk]), follow=True)

        self.assertEqual(booking_success_response.status_code, 200)

        dashboard_url_tier_one_invites_sent_with_booking_pk = (
            reverse_querystring("dashboard", args=[self.user_profile.slug],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "tier_one",
                                    "subsection": "invites_sent",
                                    "filter": test_booking.pk
                                }))

        response = self.client.get(
            dashboard_url_tier_one_invites_sent_with_booking_pk)
        self.assertEqual(response.status_code, 200)

    def test_invitation_in_dashboard_redirect_from_clicking_notification(self):

        username = "test"
        password = "test"
        email = "test"

        invite_sender = create_test_user(username, password, email)
        invite_sender_profile = get_object_or_404(
            UserProfile, user__username=invite_sender)

        test_invitation = create_test_invitation(
            invite_sender_profile, self.user_profile)
        retrieved_invitation = Invitation.objects.get(pk=test_invitation.pk)
        retrieved_invitation.is_accepted = True
        retrieved_invitation.save()

        invitation_notification = Notification.objects.get(
            notification_sender=invite_sender_profile)

        response = self.client.get(
            reverse("invite_received_notification",
                    args=[invitation_notification.pk, test_invitation.pk]),
            follow=True)

        dashboard_url_with_invitation_pk_as_filter = reverse_querystring(
            "dashboard", args=[self.user_profile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_one",
                "subsection": "invites_received",
                "filter": test_invitation.pk
            }
        )

        self.assertRedirects(
            response, dashboard_url_with_invitation_pk_as_filter,
            status_code=302, target_status_code=200)
        self.assertTrue(test_invitation in
                        response.context["invitations_received"])

    def test_filter_in_URL_query_from_booking_app(self):
        """
        Test visiting Dashboard Jobs page from Booking Success/
        Detail Page.

        Confirm that the BookingID is present in the URL query
        params when visiting from the Booking Success/Detail page.
        """

        # Create mock user to act as invitation sender.
        username = "invite_sender"
        password = "inviter_password"
        email = "inviter_email@invite.com"

        test_invite_sender = create_test_user(username, password, email)

        # Get UserProfile for Invitation Sender to tie to Invitation object.
        test_invitesender_userprofile = get_object_or_404(
            UserProfile, user=test_invite_sender)

        # Create invitation.
        test_invitation = Invitation.objects.create(
            invite_sender=test_invitesender_userprofile,
            invite_receiver=self.user_profile,
            event_name="test_event",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime=datetime.datetime.now(),
            fee=150.00,
            additional_info="test_additional_info"
        )

        # Accepting an invitation creates a booking object.
        test_invitation.is_accepted = True
        test_invitation.save()

        test_booking = Booking.objects.get(
            related_invitation__event_name="test_event"
        )

        # Set "booking_details_sent" attribute to true
        # in order to visit booking detail page.
        test_booking.booking_details_sent = True
        test_booking.save()

        booking_detail_url = f"/bookings/booking_detail/{test_booking.pk}"

        # Visit the booking detail page.
        response = self.client.get(booking_detail_url, follow=True)
        self.assertEqual(response.status_code, 200)

        # Define the URL for the Dashboard "Jobs" page, with booking ID in
        # filter query param.
        dashboard_url = reverse_querystring(
            "dashboard", args=[self.user_profile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_one",
                "subsection": "invites_received",
                "filter": test_booking.pk
            })

        # Define the booking success/detail view as the referer.
        dashboard_get_header = {
            "HTTP_REFERER": booking_detail_url
        }

        # Visit Dashboard page.
        response = self.client.get(dashboard_url, **dashboard_get_header)

        # Get the booking ID from the filter query to act as
        # control against booking ID.
        filter_query = "".join(
            response.request["QUERY_STRING"].split("&")[-1:]).split("=")[-1:]
        filter_number = int("".join(filter_query)[-1:])

        # Assert that the redirect returns the correct values.
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["current_filter"], test_booking.pk)
        self.assertTrue("filter" in response.request["QUERY_STRING"])
        self.assertEqual(filter_number, test_booking.pk)

    def test_delete_account_GET(self):
        """
        Confirm that the GET request to delete account returns
        a successful response.
        """
        response = self.client.get(self.delete_account_url, follow=True)
        self.assertRedirects(
            response, reverse("home"), status_code=302, target_status_code=200)

    def test_delete_account_redirect_for_unauthorized_user(self):
        """
        Confirm that an unauthorized user cannot delete another
        member's account by manually typing in the URL.
        """

        username = "test"
        password = "test"
        email = "test"

        authorized_user = create_test_user(username, password, email)
        authorized_user_profile = get_object_or_404(
            UserProfile, user=authorized_user)

        # self.client is acting as unauthorized user
        response = self.client.get(
            reverse("delete_account", args=[authorized_user_profile.pk]))
        messages = list(get_messages(response.wsgi_request))
        control_msg = "You can't delete another member's profile!"

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages[0]), control_msg)

    def test_delete_stripe_customer(self):
        """
        Confirm that member's stripe account is deleted
        when delete_account view is called.
        """

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.Customer.create(
            email=self.user.email
        )

        response = delete_stripe_customer(self.user.email)
        self.assertEqual(response.status_code, 200)

# ------------------------------------------------------------


class TestProfileViewPOSTMethods(TestCase):
    def setUp(self):
        username = "test_user"
        password = "abcde12345"
        email = "test@test.com"

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        self.user_profile = get_object_or_404(
            UserProfile, user=self.user)

        self.client = Client()

        self.client.login(
            username=username, password=password)

        self.edit_profile_url = reverse("edit_profile")
        self.upload_audio_url = reverse("upload_audio", args=[self.user])
        self.upload_unavailable_dates_url = reverse(
            "upload_unavailability", args=[self.user_profile.pk])
        self.profile_url = reverse("profile", args=[self.user])

    def test_profile_url_review_POST(self):
        """
        Test Review POST in Profile Page.

        Confirm that a successful POST returns
        a redirect back to the user's profile page.

        """

        # Create a mock user to act as review sender.
        username_2 = "test_user2"
        password_2 = "abcde12345"
        email_2 = "test2@test.com"

        self.user_2 = create_test_user(username_2, password_2, email_2)

        self.user_profile.first_name = "Testing"

        self.user_profile_2 = get_object_or_404(
            UserProfile, user=self.user_2)

        post_data = {
            "review_content": "test",
            "rating": 1
        }

        # Request Factory required to POST request to class based view.
        request_factory = RequestFactory()
        request = request_factory.post(self.profile_url, post_data)
        request.user = self.user_2

        # Session and Message MiddleWare required as Request Factory
        # doesn't support them out-of-the-box.
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        # Create request and confirm succesful status codes.
        response = ProfileView.as_view()(request, user_name=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "success_msg" in str(response.content, encoding="utf-8"))

    def test_profile_url_review_invalid_POST_returns_JSON_response(self):

        # Create a mock user to act as review sender.
        username_2 = "test_user2"
        password_2 = "abcde12345"
        email_2 = "test2@test.com"

        self.user_2 = create_test_user(username_2, password_2, email_2)
        user_profile_2 = get_object_or_404(UserProfile,
                                           user__username=self.user_2)

        # POST invalid data as review content
        post_data = {
            "review_content": 1,
            "rating": 1
        }

        # Request Factory required to POST request to class based view.
        request_factory = RequestFactory()
        request = request_factory.post(self.profile_url, post_data)
        request.user = self.user_2

        # Session and Message MiddleWare required as Request Factory
        # doesn't support them out-of-the-box.
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = ProfileView.as_view()(request, user_name=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "errors" in str(response.content, encoding="utf-8"))

    def test_user_profile_form_POST_success(self):
        """
        Confirm that the POST request to Edit Profile page
        returns a successful response.
        """
        session = self.client.session

        # GET request to retrieve context
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 200)

        # Create Instrument Object to add to POST data
        test_instrument = Instrument.objects.create(
            instrument_name="test_instrument"
        )

        # Create Genre Object to add to POST data
        test_genre = Genre.objects.create(
            genre_name="test_genre"
        )

        # Define POST data
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "city": "test_city",
            "country": "GB",
            "instruments_played": [test_instrument],
            "genres": [test_genre],
            "user_info": "test user info"
        }

        # Define Management Form for Equipment Formset
        # https://stackoverflow.com/questions/1630754/django-formset-unit-test
        management_form = response.context["equipment_formset"].management_form

        for i in ['TOTAL_FORMS', 'INITIAL_FORMS',
                  'MIN_NUM_FORMS', 'MAX_NUM_FORMS']:
            data['%s-%s' % (management_form.prefix, i)] = (
                management_form[i].value())

        for i in range(
                response.context['equipment_formset'].total_form_count()):
            # get form index 'i'
            current_form = response.context['equipment_formset'].forms[i]

        # retrieve all the fields
        for field_name in current_form.fields:
            value = current_form[field_name].value()
            data['%s-%s' % (current_form.prefix, field_name)] = (
                value if value is not None else '')

        # Post data to Edit Profile URL and confirm successful response.
        response = self.client.post(reverse("edit_profile"), data)
        self.assertEqual(response.status_code, 200)

    # Override MEDIA_ROOT for testing
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_audio_POST_success(self):
        """
        Create an Audio File and post to upload_audio view,
        and confirm a successful response.
        """

        test_audiofile = TemporaryUploadedFile(
            "test_audio.mp3", size=1024,
            charset="utf-8", content_type="audio/mpeg")

        file_data = {
            "audio[0]": test_audiofile,
        }

        response = self.client.post(self.upload_audio_url, file_data)
        self.assertEqual(response.status_code, 200)

    # Override MEDIA_ROOT for testing
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_audio_POST_delete_file(self):
        """
        Create an audio file and confirm that the
        alternative "delete" method in upload_audio view
        deletes the audio file object, and returns a successful
        response.
        """

        file = tempfile.NamedTemporaryFile(suffix=".mp3").name

        test_audiofile = AudioFile.objects.create(
            file=file,
            related_user=self.user_profile
        )

        # POST data - Request: 2 tells view to look for object
        # alreadt in user_profile's AudioFile table.
        file_data = {
            "filename": test_audiofile.file.name,
            "request": 2
        }

        # Confirm that the POST request returns successful response.
        response = self.client.post(self.upload_audio_url, file_data)
        self.assertEqual(response.status_code, 200)

    def test_upload_unavailable_dates_POST(self):
        """
        Create an array of date strings to post
        to upload_unavailable_dates view.

        Confirm a successful response from
        the POST request.
        """
        date_list = [
            "2022-03-22",
            "2022-03-23",
            "2022-03-24",
            "2022-03-25",
            "2022-03-26",
        ]

        data = {
            "date_array[]": date_list
        }

        response = self.client.post(self.upload_unavailable_dates_url, data)

        self.assertEqual(response.status_code, 200)

    def test_upload_unavailable_dates_POST_deletes_date(self):
        """
        Create an UnavailableDate object tied to the UserProfile
        and confirm that the view deletes the UnavailableDate object
        if it finds the date already in the User Profile's Unavailable
        Date table.
        """

        # Create Date object
        UnavailableDate.objects.create(
            date=datetime.date.today(),
            related_user=self.user_profile
        )

        # Define the date to remove
        date_to_remove = "2022-03-23"

        data = {
            "event_to_remove": date_to_remove,
            "request": 2
        }

        # Confrim a successful response
        response = self.client.post(self.upload_unavailable_dates_url, data)
        self.assertEqual(response.status_code, 200)

        # Confirm that the date is indeed removed from
        # the user profile's collection.
        testusers_unavailable_dates = self.user_profile.unavailable_user.all()
        self.assertFalse(date_to_remove in testusers_unavailable_dates)
