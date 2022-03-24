from django.test import TestCase, Client, RequestFactory
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.db.models.manager import Manager
from django.core.files.uploadedfile import SimpleUploadedFile


from profiles.models import UserProfile, Instrument, Genre
from .models import Job
from .views import post_job, EditJobView, confirm_job_offer

from test_helpers import create_test_user

from social.functions import reverse_querystring

from django.utils import timezone
import json

class TestDeplistView(TestCase):
    """
    Unit Testing - DepList View

    Test the query methods and that the view returns
    the objects successfully with a 200 status code.

    Confirm that a user can search and filter objects
    by instrument and genre.

    """
    def setUp(self):
        """
        Create a test user.
        """
        username = "test_user_1"
        password = "test_password_1"
        email = "test_email_1"

        self.test_user = create_test_user(username, password, email)
        self.test_user_profile = get_object_or_404(UserProfile, user=self.test_user)

        # Instantiate the client to make requests.
        self.client = Client()

    def test_get_queryset(self):

        # Create a test instrument to use as filter parameter.
        test_instrument = Instrument.objects.create(
            instrument_name="test_instrument",
        )

        # Create a test genre to use as filter parameter.
        test_genre = Genre.objects.create(
            genre_name="test_genre"
        )

        test_instrument = Instrument.objects.get(instrument_name=test_instrument.instrument_name)
        test_genre = Genre.objects.get(genre_name=test_genre.genre_name)

        # Add test instrument and genre to the test_user_profile object,
        # which should be returned in queryset upon searching by this instrument
        # and/or genre.
        self.test_user_profile.instruments_played.add(test_instrument)
        self.test_user_profile.genres.add(test_genre)
        self.test_user_profile.save()

        reverse_query_string = reverse_querystring("dep_list", query_kwargs={
            "instrument": "test_instrument",
            "genre": "test_genre",
        })

        # Determine a successful response, and the context contains the correct query
        # and context.
        response = self.client.get(reverse_query_string)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["instrument"], "test_instrument")
        self.assertTrue(response.context["genre"], "test_genre")
        self.assertTrue(test_instrument in response.context["instrument_list"])
        self.assertTrue(self.test_user_profile in response.context["dep_collection"])


class TestJobListView(TestCase):
    """
    Unit Testing - Job List

    Test all GET and POST methods that comprise of the Job List View.
    """
    def setUp(self):
        """
        First Test User
        """
        self.username_1 = "test_user_1"
        self.password_1 = "test_password_1"
        self.email_1 = "test_email_1"

        self.test_user_1 = create_test_user(self.username_1, self.password_1, self.email_1)
        self.test_user_profile_1 = get_object_or_404(UserProfile, user=self.test_user_1)

        """
        Second Test User
        """
        self.username_2 = "test_user_2"
        self.password_2 = "test_password_2"
        self.email_2 = "test_email_2"

        self.test_user_2 = create_test_user(self.username_2, self.password_2, self.email_2)
        self.test_user_profile_2 = get_object_or_404(UserProfile, user=self.test_user_2)

        self.test_job = Job.objects.create(
            job_poster=self.test_user_profile_1,
            job_title="test",
            event_name="test",
            artist_name="test",
            event_datetime=timezone.now(),
            fee=150.00,
            job_description="test"
        )


        """
        Instantiate the Client to make requests
        """
        self.client = Client()

    def test_joblist_page_get(self):
        """
        Confirm that the dep_list view responds successfully,
        and uses the correct template.
        """
        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("jobs/dep_list.html")

    def test_currentuser_joblist_get(self):
        """
        Confirm that a user's list of job interests
        are being retrieved and passed into context.
        """

        test_job = self.test_job

        test_job.interested_member.add(self.test_user_profile_2)
        test_job.save()

        logged_in = self.client.login(username=self.username_2, password=self.password_2)
        self.assertTrue(logged_in)

        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_job in response.context["current_users_jobs"])

        
    def test_job_post(self):
        """
        Make a test POST request to the view's 'post' method,
        and confirm that the view returns a successful response.
        """

        self.test_user_profile_1.subscription_chosen = True
        self.test_user_profile_1.is_paid = True
        self.test_user_profile_1.save()

        # Test POST request
        test_post_dict = {
            "job_title": "test_job",
            "event_name": "test_event",
            "artist_name": "test_artist",
            "job_description": "test_job_desc",
            "fee": 150.00,
            "event_city": "test_city",
            "event_country": "GB",
            "event_datetime": "22/03/2022 17:01:00"
        }
        
        # Instantiate the request factory, along with the
        # session and message middleware required in order
        # for request factory to function.
        request_factory = RequestFactory()
        request = request_factory.post(reverse("post_job"), test_post_dict)
        request.user = self.test_user_profile_1
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        # 
        response = post_job(request)
        self.assertEqual(response.status_code, 302)

    
    def test_job_post_redirect_if_user_not_paid(self):
        """
        Confirm that an unpaid member is redirected away
        from job_post view, in the case they try to
        access the view manually through URL.
        """
        self.test_user_profile_1.subscription_chosen = True
        self.test_user_profile_1.save()

        # Request Factory needed for Unit Test.
        request_factory = RequestFactory()
        request = request_factory.get(reverse("post_job"))
        request.user = self.test_user_profile_1
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = post_job(request)
        self.assertEqual(response.status_code, 302)

    def test_job_post_redirect_if_form_invalid(self):
        """
        Confirm that a post request containing invalid
        data returns the appropriate response.
        """
        self.test_user_profile_1.subscription_chosen = True
        self.test_user_profile_1.is_paid = True
        self.test_user_profile_1.save()

        test_post_dict = {
            "job_title": "111",
            "event_name": "test_event",
            "artist_name": "test_artist",
            "job_description": "test_job_desc",
            "fee": 150.00,
            "event_country": "GB",
            "event_datetime": "22/03/2022 17:01:00"
        }

        # Request Factory and Session/Message Middleware
        request_factory = RequestFactory()
        request = request_factory.post(reverse("post_job"), test_post_dict)
        request.user = self.test_user_profile_1
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = post_job(request)
        self.assertEqual(response.status_code, 302)

    def test_edit_job_GET(self):
        """
        Test the GET request to access the EditJob view,
        and confirm that the view returns a successful
        200 response.
        """
        self.client.login(
            username=self.username_1,
            password=self.password_2
        )

        test_job = self.test_job

        request_factory = RequestFactory()
        request = request_factory.get(reverse("edit_job", args=[test_job.pk]))
        request.user = self.test_user_1
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = EditJobView.as_view()(request, job_id=test_job.pk)

        self.assertEqual(response.status_code, 200)

    def test_edit_job_redirect_for_unauthorized_user(self):
        """
        Confirm that the Edit Job view is restricted only
        to the user who owns the Job object.
        """
        
        self.client.login(
            username=self.username_2,
            password=self.password_2
        )

        test_job = self.test_job

        # Request Factory and Session/Message Middleware
        request_factory = RequestFactory()
        request = request_factory.get(reverse("edit_job", args=[test_job.pk]))
        request.user = self.test_user_2
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = EditJobView.as_view()(request, job_id=test_job.pk)

        self.assertEqual(response.status_code, 302)

    def test_edit_job_POST_request(self):
        """
        Test the POST method of the EditJobView, and confirm
        that the method returns a successful response with the
        appropriate redirects.
        """
        self.client.login(
            username=self.username_1,
            password=self.password_1
        )

        test_job = self.test_job
        
        test_job_post_edit_dict = {
            "job_title": "test_job",
            "event_name": "test_event",
            "artist_name": "test_artist",
            "event_city": "test_city",
            "event_country": "GB",
            "job_description": "test_job_description",
            "event_datetime": timezone.now(),
            "fee": 200.00
        }

        request_factory = RequestFactory()
        request = request_factory.post(
            reverse("edit_job", args=[test_job.pk]), test_job_post_edit_dict)
        request.user = self.test_user_1
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = EditJobView.as_view()(request, job_id=self.test_job.pk)

        self.assertEqual(response.status_code, 302)

    def test_job_delete(self):
        """
        Test the Delete Job view, and confirm that a successful
        redirect is returned, to the appropriate page, and that
        the test job is indeed removed from the Job queryset.
        """
        self.client.login(
            username=self.username_1,
            password=self.password_1
        )

        test_job = self.test_job 

        response = self.client.get(reverse("delete_job", args=[test_job.pk]), follow=True)
        self.assertRedirects(response, reverse("job_list"), status_code=302, target_status_code=200)
        
        all_jobs = Job.objects.all()
        self.assertFalse(test_job in all_jobs)


    def test_register_interest(self):
        """
        Test the view to register interest in a job,
        and confirm a successful 302 response, with 
        redirect to the appropriate page.

        Confirm that the test_user_profile_2 object
        is in the collection of Job's "interested_members"
        """
        test_job = self.test_job


        self.test_user_profile_2.subscription_chosen = True
        self.test_user_profile_2.is_paid = True
        self.test_user_profile_2.save()

        response = self.client.get(
            reverse("register_interest", args=[test_job.pk, self.test_user_2]), follow=True)
        
        self.assertRedirects(response, reverse("job_list"), status_code=302, target_status_code=200)
        self.assertTrue(self.test_user_profile_2 in test_job.interested_member.all())
    
    def test_register_interest_redirect_if_user_not_paid(self):
        """
        Confirm that an unpaid user is redirected from view
        if they attempt to access manually from the URL.

        Confirm a successful redirect to the appropriate page,
        and that the user hasn't been added to the Job's collection
        of interested members.
        """

        test_job = self.test_job

        response = self.client.get(
            reverse("register_interest", args=[test_job.pk, self.test_user_2]), follow=True)

        self.assertRedirects(response, reverse("job_list"), status_code=302, target_status_code=200)
        self.assertTrue(self.test_user_profile_2 not in test_job.interested_member.all())
        self.assertEqual(len(test_job.interested_member.all()), 0)

    def test_job_confirmation(self):
        """
        Assure that a user can successfully confirm
        an interested member on a job, and that the view
        redirects successfully, to the appropriate page.
        """

        test_job = self.test_job
        confirmed_user = self.test_user_2

        request_factory = RequestFactory()
        request = request_factory.get(reverse("confirm_job_offer", args=[test_job.pk, confirmed_user]))
        request.user = self.test_user_1
        session_middleware = SessionMiddleware(lambda x: x)
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(lambda x: x)
        message_middleware.process_request(request)
        request.session.save()

        response = confirm_job_offer(request, test_job.pk, confirmed_user)

        self.assertEqual(response.status_code, 302)

    def test_get_interested_members(self):
        """
        Unit Test - Get Interested Members

        Test the AJAX view which returns a list of members who have marked
        interest in taking a particular Job advertised on the Job List Page.

        Confirm that the view correctly returns the member's details
        as a JSON object. 

        Confirm that all low-level details, such as:
        
        1. First Name
        2. Last Name
        3. City
        4. Country
        5. Profile Image

        are being returned correctly.
        """
        # Test that the interested member's instruments are
        # returned in the view.

        # Create a test instrument and add it to User Profile 2's
        # list of instruments played.
        test_instrument = Instrument.objects.create(
            instrument_name="test_instrument"
        )
        self.test_user_profile_2.instruments_played.add(test_instrument)

        test_profile_image = SimpleUploadedFile(
            name="test_image.jpg", content=b"", content_type="image/jpeg")

        # Give the test user a first and last name
        self.test_user_profile_2.first_name = "test fname"
        self.test_user_profile_2.last_name = "test lname"
        self.test_user_profile_2.city = "test city"
        self.test_user_profile_2.country = "GB"
        self.test_user_profile_2.profile_image = test_profile_image
        self.test_user_profile_2.save()

        # Add the test user to the collection of interested members
        # for a job.
        test_job_object = get_object_or_404(Job, pk=self.test_job.pk)
        test_job_object.interested_member.add(self.test_user_profile_2)
        test_job_object.save()

        response = self.client.get(reverse("get_interested_members", args=[self.test_job.pk]))
        print(response.content)

        instrument_array = []
        instrument_array.append(test_instrument.instrument_name)

        # Prepare the returned data to compare against the values set above.
        control_fname = json.loads(response.content)["member_details"][0]["first_name"]
        control_lname = json.loads(response.content)["member_details"][0]["last_name"]
        control_instruments_played = json.loads(response.content)["member_details"][0]["instruments_played"]
        control_job_id = json.loads(response.content)["member_details"][0]["job_id"]
        control_username = json.loads(response.content)["member_details"][0]["username"]
        control_city = json.loads(response.content)["member_details"][0]["city"]
        control_country = json.loads(response.content)["member_details"][0]["country"]
        control_profile_img = json.loads(response.content)["member_details"][0]["profile_image"]


        # Determine and confirm a successful response with all data present.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(control_fname, self.test_user_profile_2.first_name)
        self.assertEqual(control_lname, self.test_user_profile_2.last_name)
        self.assertEqual(control_city, self.test_user_profile_2.city)
        self.assertEqual(control_country, "United Kingdom")
        self.assertEqual(control_profile_img, self.test_user_profile_2.profile_image.url)
        self.assertEqual(control_instruments_played, instrument_array)
        self.assertEqual(control_job_id, self.test_job.pk)
        self.assertEqual(control_username, self.test_user_2.username)



