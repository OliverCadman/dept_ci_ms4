from django.test import TestCase, Client, RequestFactory
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages import get_messages
from django.utils import timezone
from django.conf import settings

from test_helpers import (
    create_test_user, create_test_invitation, create_test_job,
    create_test_message)

from profiles.models import UserProfile
from social.models import Message
from social.functions import reverse_querystring
from jobs.models import Job

from .views import invitation_form_view, accept_invitation, GeneratePDFFile
from .models import Invitation, Booking

from dateutil import parser
import json
import tempfile


class TestInvitationPOSTView(TestCase):
    def setUp(self):
        """
        Set up two test User objects along with 
        User Profiles, and log Test User 1 in.
        """

        username = "test"
        password = "test"
        email = "test"

        self.test_user = create_test_user(username, password, email)
        self.test_user_profile = get_object_or_404(
            UserProfile, user__username=self.test_user)

        username2 = "test2"
        password2= "test2"
        email2 = "test2"

        self.test_user2 = create_test_user(username2, password2, email2)
        self.test_user_profile_2 = get_object_or_404(
            UserProfile, user__username=self.test_user2)

        # Instantiate the client and login
        self.client = Client()
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_invitation_view_POST(self):
        """
        Confirm that the Invitation POST request
        returns a successful response.
        """

        invite_receiver = self.test_user2

        test_post = {
            "invite_sender": self.test_user_profile,
            "event_name": "test_event",
            "artist_name": "test_artist",
            "event_city": "test_city",
            "event_country": "GB",
            "event_datetime": "22/03/2022 10:15:00",
            "fee": 100.00,
            "additional_info": "test_info"
        }

        request_factory = RequestFactory()
        request = request_factory.post(reverse("invitation"), test_post)
        request.user = self.test_user

        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session["invited_username"] = invite_receiver.username
        request.session.save()  

        response = invitation_form_view(request)
        self.assertEqual(response.status_code, 302)

    def test_invitation_post_invalid(self):
        """
        Confirm that a post with invalid data returns
        the appropriate JSON response, containing
        form errors.
        """

        invite_receiver = self.test_user2

        test_post_invalid = {
            "invite_sender": self.test_user_profile,
            "event_name": 123,
            "artist_name": "test_artist",
            "event_city": "test_city",
            "event_country": "GB",
            "event_datetime": "22/03/2022 10:15:00",
            "fee": 100.00,
            "additional_info": "test_info"
        }

        request_factory = RequestFactory()
        request = request_factory.post(reverse("invitation"), test_post_invalid)
        request.user = self.test_user

        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session["invited_username"] = invite_receiver.username
        request.session.save()  

        response = invitation_form_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("errors" in str(response.content, encoding="utf-8"))

# -------------------------------------------
class TestEditInvitationPOSTView(TestCase):
    def setUp(self):
        """
        Setup two test users and user profiles, and log
        first test user in.
        """
        username = "test"
        password = "test"
        email = "test"

        self.test_user = create_test_user(username, password, email)
        self.test_user_profile = get_object_or_404(
            UserProfile, user__username=self.test_user)

        username2 = "test2"
        password2= "test2"
        email2 = "test2"

        self.test_user2 = create_test_user(username2, password2, email2)
        self.test_user_profile_2 = get_object_or_404(
            UserProfile, user__username=self.test_user2)

        # Instantiate the client and login
        self.client = Client()
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_restricted_access_to_edit_invitation_view(self):
        """
        Confirm that an unauthorized user visiting the Edit Invitation
        page is redirected back home.
        """

        # The unauthorized user
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()
        
        invitation = Invitation.objects.create(
            invite_sender = self.test_user_profile_2,
            invite_receiver= self.test_user_profile,
            event_name="test",
            artist_name="test",
            event_city="test",
            event_country="GB",
            event_datetime=timezone.now(),
            additional_info="test"
        )

        response = self.client.get(reverse("edit_invitation", args=[invitation.pk]), follow=True)
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

    
    def test_edit_invitation_POST_method(self):
        """
        Confirm a successful response from the Edit Invitation's
        POST method, along with correct success message.
        """
        datetime = "23-03-2022 12:16:21"
        parsed_datetime = parser.parse(datetime)
        
        # Create an invitation to edit
        test_invitation = Invitation.objects.create(
            invite_sender=self.test_user_profile,
            invite_receiver=self.test_user_profile_2,
            event_name="test_event",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime= parsed_datetime,
            fee=150.00,
            additional_info="test_additional_info"
        )

        # Edit post request object
        test_edit = {
            "event_name": "test_edit",
            "artist_name": "test_edit",
            "event_city": "test_edit",
            "event_country": "GB",
            "event_datetime": "23-03-2022 12:16:21",
            "fee": 1000.00,
            "additional_info": "test_edit"
        }

        response = self.client.post(
            reverse("edit_invitation", args=[test_invitation.pk]), test_edit)
        
        messages = list(get_messages(response.wsgi_request))
        control_msg = "Invitation form edited"
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages[0]), control_msg)

# --------------------------------------------------
class TestBookingViewGETMethods(TestCase):
    """
    Test all Booking View GET Methods
    """
    
    def setUp(self):
        """
        Set up two test User objects along with 
        User Profiles, and log Test User 1 in.
        """

        username = "test"
        password = "test"
        email = "test"

        self.test_user = create_test_user(username, password, email)
        self.test_user_profile = get_object_or_404(
            UserProfile, user__username=self.test_user)

        username2 = "test2"
        password2= "test2"
        email2 = "test2"

        self.test_user2 = create_test_user(username2, password2, email2)
        self.test_user_profile_2 = get_object_or_404(
            UserProfile, user__username=self.test_user2)

        # Instantiate the client and login
        self.client = Client()
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_get_invitation_messages(self):
        """
        Test AJAX handler to return messages related to
        a given Invitation, to be displayed in modal window
        in user's dashboard.

        Confirm that the view returns a successful
        JsonResponse and:

        1. The message returned matches the message created
           in the Message object below.
        2. The returned message_sender ID matches the UserProfile
           object related to the created Message object.
        3. The returned  message_receiver ID matches the UserProfile
            object related to the created Message object (as message receiver)
        """

        test_invitation = create_test_invitation(
            self.test_user_profile, self.test_user_profile_2)
        
        test_message = Message.objects.create(
            message_sender=self.test_user_profile,
            message_receiver=self.test_user_profile_2,
            invitation_id=test_invitation,
            message="test_message"
        )

        # Referal needed as the view relies on knowing the referal URL
        referer_url = "http://127.0.0.1:8000" + reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_one",
                "subsection": "invites_sent",
                "filter": "all"
            }
        )

        response = self.client.get(
            reverse("get_invitation_messages", args=[test_invitation.pk]),
                    HTTP_REFERER=referer_url)

        # Confirm a successful response
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)

        # Extract the message context, and UserProfiles related to it
        json_returned_message = json_response["messages"][0]["message"]
        message_sender_id = json_response["messages"][0]["message_sender"]
        message_receiver_id = json_response["messages"][0]["message_receiver"]

        # Confirm the returned values match all the appropriate fields of Message object.
        message_sender_profile = get_object_or_404(UserProfile, pk=message_sender_id)
        message_receiver_profile = get_object_or_404(UserProfile, pk=message_receiver_id)
        self.assertEqual(json_returned_message, test_message.message)
        self.assertEqual(message_sender_profile, self.test_user_profile)
        self.assertEqual(message_receiver_profile, self.test_user_profile_2)

    
    def test_get_job_messages(self):
        """
        Test AJAX handler to return messages related to
        a given Job, to be displayed in modal window
        in user's dashboard.

        Confirm that the view returns a successful
        JsonResponse and:

        1. The message returned matches the message created
           in the Message object below.
        2. The returned message_sender ID matches the UserProfile
           object related to the created Message object.
        3. The returned  message_receiver ID matches the UserProfile
            object related to the created Message object (as message receiver)
        """

        test_job = create_test_job(self.test_user_profile)
        test_job_object = Job.objects.get(pk=test_job.pk)

        test_job_object.interested_member.add(self.test_user_profile_2)
        test_job_object.save()

        test_message = create_test_message(
            self.test_user_profile,
            self.test_user_profile_2,
            related_job=test_job_object,
            related_invitation=None
        )

         # Referal needed as the view relies on knowing the referal URL
        referer_url = "http://127.0.0.1:8000" + reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_two",
                "subsection": "posted_jobs",
                "filter": "all"
            }
        )

        response = self.client.get(
            reverse("get_invitation_messages", args=[test_job.pk]),
                    HTTP_REFERER=referer_url)

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)

        # Extract the message context, and UserProfiles related to it
        json_returned_message = json_response["messages"][0]["message"]
        message_sender_id = json_response["messages"][0]["message_sender"]
        message_receiver_id = json_response["messages"][0]["message_receiver"]

        # Confirm the returned values match all the appropriate fields of Message object.
        message_sender_profile = get_object_or_404(UserProfile, pk=message_sender_id)
        message_receiver_profile = get_object_or_404(UserProfile, pk=message_receiver_id)
        self.assertEqual(json_returned_message, test_message.message)
        self.assertEqual(message_sender_profile, self.test_user_profile)
        self.assertEqual(message_receiver_profile, self.test_user_profile_2)

    
    def test_get_invitation_success_with_no_messages(self):
        """
        Confirm that the get_invitation_messages view
        returns a successful response when no messages
        exist.
        """

        test_job = create_test_job(self.test_user_profile)

         # Referal needed as the view relies on knowing the referal URL
        referer_url = "http://127.0.0.1:8000" + reverse_querystring(
            "dashboard", args=[self.test_user_profile.slug],
            query_kwargs={
                "page": "jobs",
                "section": "tier_two",
                "subsection": "posted_jobs",
                "filter": "all"
            }
        )

        response = self.client.get(
            reverse("get_invitation_messages", args=[test_job.pk]),
                    HTTP_REFERER=referer_url)

        self.assertEqual(response.status_code, 200)

    
    def test_accept_invitation(self):
        """
        Test Accept Invitation View to confirm
        that it responds successfully.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile_2,
            self.test_user_profile
        )

        test_invitation_object = Invitation.objects.get(pk=test_invitation.pk)

        # User RequestFactory to create mock request user
        # to act as invitation receiver.
        request_factory = RequestFactory()
        request = request_factory.get(
            reverse("accept_invitation",  args=[test_invitation_object.pk]))

        request.user = self.test_user

        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()  

        response = accept_invitation(request, test_invitation_object.pk)
        self.assertEqual(response.status_code, 302)

    
    def test_decline_invitation(self):
        """
        Test Decline Invitation View, and confirm
        that the view returns a successful redirect,
        with the appropriate success message.

        Further confirmation that there are no invitations
        in the queryset once the test has been completed.
        """

        test_invitation = create_test_invitation(
            self.test_user_profile_2,
            self.test_user_profile
        )

        invitation_queryset = Invitation.objects.all()

        response = self.client.get(reverse("decline_invitation", args=[test_invitation.pk]))

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        success_msg = "You declined test2's invitation."

        self.assertEqual(str(messages[0]), success_msg)
        self.assertEqual(len(invitation_queryset), 0)

    def test_delete_invitation(self):
        """
        Test Delete Invitation View, and confirm
        that the created invitation is deleted, with
        a successful 302 response to user's dashboard. 

        Confirm that the appropriate success message
        is returned, and that the length of the Invitation
        queryset is zero.
        """
        self.test_user_profile_2.subscription_chosen = True
        self.test_user_profile_2.save()

        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile_2
        )

        invitation_queryset = Invitation.objects.all()

        response = self.client.get(reverse("delete_invitation", args=[test_invitation.pk]))
        self.assertRedirects(response, reverse("dashboard", args=[self.test_user_profile.slug]),
                             status_code=302, target_status_code=200)
        
        messages = list(get_messages(response.wsgi_request))
        success_msg = "Invitation deleted."
        self.assertEqual(str(messages[0]), success_msg)
        self.assertEqual(len(invitation_queryset), 0)

    
    def test_booking_form_view_redirects_for_unauthorized_user(self):
        """
        Confirm that access to the page is restricted to the user who
        owns the Invitation object.

        Confirm that the appropriate message is displayed.
        """

        # Unauthorized User
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()

        # Create test invitation
        test_invitation = create_test_invitation(
            self.test_user_profile_2,
            self.test_user_profile
        )

        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)

        test_invitation_object.is_accepted = True
        test_invitation_object.save()

        response = self.client.get(reverse("booking_form", args=[test_invitation.pk]), follow=True)

        messages = list(get_messages(response.wsgi_request))
        warning_msg = "You may not browse another member's booking."

        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), warning_msg)

    def test_tiertwo_booking_form_view_redirects_for_unauthorized_user(self):
        """
        Confirm that access to the tier_two booking form page is restricted 
        to the user whoowns the Job object.

        Confirm that the appropriate message is displayed.
        """

        # Unauthorized User
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()

        # Create test job
        test_job = create_test_job(
            self.test_user_profile_2
        )

        test_job_object = get_object_or_404(Job, pk=test_job.pk)
        test_job_object.confirmed_member = self.test_user_profile

        response = self.client.get(reverse("tier_two_booking_form", args=[test_job.pk]), follow=True)

        messages = list(get_messages(response.wsgi_request))
        warning_msg = "You may not browse another member's booking."

        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), warning_msg)

    def test_booking_success_redirect_for_unauthorized_user(self):
        """
        Confirm that the Booking Success view is restricted only
        to the users associated with the booking, with a successful
        response and redirect to the home page, with the appropriate
        error message.
        """

        username3 = "test3"
        password3 = "test3"
        email3 = "test3@test.com"

        # Create another user profile to act as authorized user
        authorized_user = create_test_user(username3, password3, email3)
        authorized_user_profile = get_object_or_404(UserProfile, user=authorized_user)

        authorized_user_profile.subscription_chosen = True
        authorized_user_profile.save()

        # self.test_user_profile1 is unauthorized and logged in.
        unauthorized_user_profile = self.test_user_profile
        unauthorized_user_profile.subscription_chosen = True
        unauthorized_user_profile.save()

        test_invitation = create_test_invitation(
            authorized_user_profile,
            self.test_user_profile_2
        )
        
        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)
        test_invitation.is_accepted = True

        # Create a booking object
        test_booking = Booking.objects.create(
            related_invitation=test_invitation,
            venue_name="test",
            street_address1="test",
            travel_provided=False,
            backline_provided=False
        )

        # Determine a successful redirect response with the appropriate error message.
        response = self.client.get(reverse("booking_success", args=[test_booking.pk]), follow=True)

        messages = list(get_messages(response.wsgi_request))
        error_msg = "You may not browse another user's booking."

        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), error_msg)

    def test_booking_detail_redirect_for_unauthorized_user(self):
        """
        Confirm that the Booking Success view is restricted only
        to the users associated with the booking, with a successful
        response and redirect to the home page, with the appropriate
        error message.
        """

        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()
 
        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile_2
        )
        
        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)
        test_invitation.is_accepted = True

        # Create a booking object
        test_booking = Booking.objects.create(
            related_invitation=test_invitation,
            venue_name="test",
            street_address1="test",
            travel_provided=False,
            backline_provided=False
        )

        test_booking_object = get_object_or_404(Booking, pk=test_booking.pk)
        test_booking_object.booking_details_sent = True
        test_booking_object.save()

        # Determine a successful redirect response with the appropriate error message.
        response = self.client.get(reverse("booking_detail", args=[test_booking.pk]), follow=True)

        messages = list(get_messages(response.wsgi_request))
        error_msg = "You may not browse another user's booking."

        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), error_msg)

    def test_generate_pdf_file_view(self):
        """
        Test PDF Generation of Booking.

        Confirm that the view returns a successful
        response with a generated PDF in the response's
        content.
        """

        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()
 
        test_invitation = create_test_invitation(
            self.test_user_profile_2,
            self.test_user_profile
        )
        

        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)
        test_invitation.is_accepted = True

        # Create a booking object
        test_booking = Booking.objects.create(
            related_invitation=test_invitation,
            venue_name="test",
            street_address1="test",
            travel_provided=False,
            backline_provided=False
        )

        # Request Factory required for class-based view
        request_factory = RequestFactory()
        request = request_factory.get(reverse("generate_pdf", args=[test_booking.pk]))
        request.user = self.test_user
        request.download = True

        # Session and Message Middleware required for Request Factory
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        request.session.save()

        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)

        kwargs = {"booking_id": test_booking.pk}

        response = GeneratePDFFile.as_view()(request, **kwargs)

        # Determine a successful response
        self.assertEqual(response.status_code, 200)

    def test_restrict_access_to_generate_pdf_file_view(self):
        """
        Test Restricted Access to Generate PDF File View

        Confirm that any user trying to access view
        who is not the booking receiver, is redirected
        back home.

        Restriction applied in the case that a user
        accesses the view manually through the URL.
        """

        # Test User Profile is the booking sender 
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()
 
        test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile_2
        )

        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)
        test_invitation.is_accepted = True
        test_invitation_object.save()

        # Create a booking object
        test_booking = Booking.objects.create(
            related_invitation=test_invitation,
            venue_name="test",
            street_address1="test",
            travel_provided=False,
            backline_provided=False
        )

        # Request factory required to access class-based view
        request_factory = RequestFactory()
        request = request_factory.get(reverse("generate_pdf", args=[test_booking.pk]))
        request.user = self.test_user

        # Session and Message Middleware required for Request Factory
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        request.session.save()

        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)

        kwargs = { "booking_id": test_booking.pk }

        response = GeneratePDFFile.as_view()(request, **kwargs)
        response.client = self.client 

        # Determine a successful redirect back to home.
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

# -------------------------------------------------
class TestBookingViewPOSTMethods(TestCase):
    """
    Test all Booking View POST methods
    """
    
    def setUp(self):
        """
        Set up two test User objects along with 
        User Profiles, and log Test User 1 in.
        """

        username = "test"
        password = "test"
        email = "test"

        self.test_user = create_test_user(username, password, email)
        self.test_user_profile = get_object_or_404(
            UserProfile, user__username=self.test_user)

        username2 = "test2"
        password2 = "test2"
        email2 = "test2"

        self.test_user2 = create_test_user(username2, password2, email2)
        self.test_user_profile2 = get_object_or_404(
            UserProfile, user__username=self.test_user2)

        # Set up a test invitation object
        self.test_invitation = create_test_invitation(
            self.test_user_profile,
            self.test_user_profile2
        )

        self.client = Client()
        logged_in = self.client.login(username=username, password=password)

    
    def test_booking_form_POST(self):
        """
        Test POST method of Booking Form view.
        Confirm a successful POST request response,
        with the appropriate redirect and success message
        displayed.
        """

        # Subscribe user in order to make a booking.
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()

        test_invitation = self.test_invitation

        # Accept the invitation to create a Booking object.
        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)
        test_invitation_object.is_accepted = True
        test_invitation_object.save()

        test_booking = get_object_or_404(Booking, related_invitation__pk=test_invitation.pk)

        # Make a GET request to get the context
        response = self.client.get(reverse("booking_form", args=[test_invitation.pk]))
        self.assertEqual(response.status_code, 200)

        test_audiofile = tempfile.NamedTemporaryFile(suffix=".mp3").name

        data = {
            "venue_name": "test_venue",
            "street_address1": "test_street_address",
            "postcode": "PR7 5RH",
            "travel_provided": True,
            "travel_info": "test_info",
            "backline_provided": True,
            "backline_info": "test_info",
        }

        # Mimic the Audio Formset
        management_form = response.context["audio_formset"].management_form

        for i in 'TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS':
            data['%s-%s' % (management_form.prefix, i)] = management_form[i].value()
        
        for i in range(response.context['audio_formset'].total_form_count()):
            # get form index 'i'
            current_form = response.context['audio_formset'].forms[i]

        # retrieve all the fields
        for field_name in current_form.fields:
            value = current_form[field_name].value()
            data['%s-%s' % (current_form.prefix, field_name)] = value if value is not None else ''

        # Post the Data to the View
        response = self.client.post(
            reverse("booking_form", args=[test_invitation.pk]), data, follow=True
        )

        # Determine a successful response with appropriate redirect and success message.
        messages = list(get_messages(response.wsgi_request))
        success_msg = "Booking Form Submitted."
        self.assertRedirects(response, reverse("booking_success", args=[test_booking.pk]),
                             status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), success_msg)
    
    def test_booking_form_POST_with_invalid_data(self):
        """
        Test the Booking Form POST with invalid data,
        and confirm a successful redirect back to the
        booking form page, with appropriate error message
        displayed.
        """

         # Subscribe user in order to make a booking.
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.save()

        test_invitation = self.test_invitation

        # Accept the invitation to create a Booking object.
        test_invitation_object = get_object_or_404(Invitation, pk=test_invitation.pk)
        test_invitation_object.is_accepted = True
        test_invitation_object.save()

        # Prepare POST request with invalid data
        invalid_data = {
            "venue_name": "111",
            "street_address1": "111",
            "travel_provided": True,
            "travel_info": "111",
            "backline_provided": True,
            "backline_info": "111"
        }

        response = self.client.post(
            reverse("booking_form", args=[test_invitation.pk]), invalid_data, follow=True)

        # Determine the appropriate redirect with error message.
        messages = list(get_messages(response.wsgi_request))
        error_msg = "Your form was invalid, please try again."

        self.assertRedirects(response, reverse("booking_form", args=[test_invitation.pk]), status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), error_msg)

    
    def test_tier_two_invitation_booking_form_POST_method(self):
        """
        Test the POST method of the booking form page
        for Tier Two bookings, and confirm that the view
        returns a successful redirect to the appropriate
        success page, and that the appropriate success
        message is displayed.
        """

        # Subsribe the user and set "is paid" to True in order 
        # to make a Tier Two booking.
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.is_paid = True
        self.test_user_profile.save()

        # Create a test job.
        test_job = create_test_job(self.test_user_profile)

        test_job_object = get_object_or_404(Job, pk=test_job.pk)

        # Tie User Profile two to test job as confirmed member.
        test_job_object.is_taken = True
        test_job_object.confirmed_member = self.test_user_profile2
        test_job_object.save()


        Booking.objects.create(
            related_job=test_job
        )

        test_booking_object = get_object_or_404(Booking, related_job=test_job)

        response = self.client.get(reverse("tier_two_booking_form", args=[test_job.pk]))
        self.assertEqual(response.status_code, 200)

        # Prepare a POST request
        data = {
            "venue_name": "test_venue",
            "street_address1": "test_street_address",
            "postcode": "PR7 5RH",
            "travel_provided": True,
            "travel_info": "test_info",
            "backline_provided": True,
            "backline_info": "test_info",
        }

         # Mimic the Audio Formset
        management_form = response.context["audio_formset"].management_form

        for i in 'TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS':
            data['%s-%s' % (management_form.prefix, i)] = management_form[i].value()
        
        for i in range(response.context['audio_formset'].total_form_count()):
            # get form index 'i'
            current_form = response.context['audio_formset'].forms[i]

        # retrieve all the fields
        for field_name in current_form.fields:
            value = current_form[field_name].value()
            data['%s-%s' % (current_form.prefix, field_name)] = value if value is not None else ''

        # Post the Data to the View
        response = self.client.post(
            reverse("tier_two_booking_form", args=[test_job.pk]), data, follow=True
        )

        # Determine a successful response with appropriate redirect and success message.
        messages = list(get_messages(response.wsgi_request))
        success_msg = "Booking Form Submitted"
        self.assertRedirects(response, reverse("booking_success", args=[test_booking_object.pk]),
                             status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), success_msg)

    def test_tier_two_booking_form_POST_with_invalid_data(self):
        """
        Test the Tier Two Booking Form POST with invalid data,
        and confirm a successful redirect back to the
        booking form page, with appropriate error message
        displayed.
        """

        # Subsribe the user and set "is paid" to True in order 
        # to make a Tier Two booking.
        self.test_user_profile.subscription_chosen = True
        self.test_user_profile.is_paid = True
        self.test_user_profile.save()

        # Create a test job.
        test_job = create_test_job(self.test_user_profile)

        test_job_object = get_object_or_404(Job, pk=test_job.pk)

        # Tie User Profile 2 to the Job and set "is taken" status to True.
        test_job_object.is_taken = True
        test_job_object.confirmed_member = self.test_user_profile2
        test_job_object.save()

        # Create a booking related to the job.
        Booking.objects.create(
            related_job=test_job
        )

        response = self.client.get(reverse("tier_two_booking_form", args=[test_job.pk]))
        self.assertEqual(response.status_code, 200)

        data = {
            "venue_name": "111",
            "street_address1": "111",
            "postcode": "111",
            "travel_provided": True,
            "travel_info": "111",
            "backline_provided": True,
            "backline_info": "111",
        }

        # Post the Data to the View
        response = self.client.post(
            reverse("tier_two_booking_form", args=[test_job.pk]), data, follow=True
        )

        # Determine a successful response with appropriate redirect and success message.
        messages = list(get_messages(response.wsgi_request))
        error_msg = "Your form was invalid, please try again."
        self.assertRedirects(response, reverse("tier_two_booking_form", args=[test_job.pk]),
                             status_code=302, target_status_code=200)
        self.assertEqual(str(messages[0]), error_msg)


