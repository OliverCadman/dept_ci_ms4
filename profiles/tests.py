from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.test.utils import tag
from django.contrib.auth import authenticate
from django.urls import reverse


from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles.models import (UserProfile, Instrument, Genre, UnavailableDate,
                             AudioFile, Equipment)

import datetime
import tempfile
from urllib.parse import urlencode


class SignInTest(TestCase):
    """
    Unit Tests for User Authentication
    """
    
    def setUp(self):
        """
        Create a test user to log in.
        """
        self.client = Client()
        self.username = "test"
        self.password = "abc123"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username=self.username,
                                                   password=self.password)

    
    def tearDown(self):
        """
        Deletes test user after unit tests are ran.
        """
        self.user.delete()

    def test_correct_details(self):
        """
        Authenticate with correct details and check if
        returned user exists, and is authenticated.
        """
        user = authenticate(username="test", password="abc123")
        self.assertTrue((user is not None) and user.is_authenticated)
    
    def test_wrong_password(self):
        """
        Authenticate with incorrect password and check if
        returned user doesn't exist, and isn't authenticated.
        """
        user = authenticate(username="test", password="wrongpassword")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        """
        Authenticate with incorrect username and check if
        returned user doesn't exist, and isn't authenticated.
        """
        user = authenticate(username="wrongusername", password="abc123")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_signin_redirect(self):
        """
        Authenticate with correct details and check if 
        returned user is redirected to the home page.
        """
        user = authenticate(username="username", password="abc123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_userprofile_created(self):
        """
        Test create_or_update_user signal to check if User Profile
        is created upon creation of user.
        """
        user_profile = UserProfile.objects.get(user__username=self.user.username)
        self.assertTrue(user_profile is not None)
    
    def test_user_logged_in(self):
        """
        Confirm that the user logs in successfully.
        """
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)
        

class TestProfileViews(TestCase):
    """
    Unit Tests for views profile views 
    """

    def setUp(self):
        """
        Create user and log them in
        """
        username = "test"
        password = "abc123"
        self.client = Client()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=username,
            password=password
        )
        self.user_profile = UserProfile.objects.get(user__username=self.user)
        self.logged_in = self.client.login(username=username, password=password)

    
    
    def test_get_profile_view(self):
        """
        Check if profile view url & params resolve with success status.
        """
        response = self.client.get(reverse("profile", args=[self.user.username]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("profiles/profile.html")

    def test_profile_view_user_context(self):
        """
        Confirm that the profile view returns the visiting client's username.
        """
        response = self.client.get(reverse("profile", args=[self.user.username]))
        self.assertEqual(response.context["user"], self.user_profile)

    def test_get_profile_edit_view(self):
        """
        Check if edit profile view resolves with success status.
        """
        response = self.client.get("/profile/edit_profile")
        self.assertEqual(response.status_code, 200)


class TestProfileModels(TestCase):
    """
    Test Class to Unit Test Profile Models
    """
    
    def setUp(self):
        """
        Create user and log them in


        Create instances of models related to user:

        - Instrument
        - Genre
        - Equipment 
        """
        username = "test"
        password = "abc123"
        self.client = Client()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=username,
            password=password
        )
        self.user_profile = UserProfile.objects.get(user__username=self.user)
        self.logged_in = self.client.login(username=username, password=password)

        self.instrument = Instrument.objects.create(
            instrument_name="test_instrument",
        )

        self.genre = Genre.objects.create(
            genre_name="test_genre"
        )

        self.equipment = Equipment.objects.create(
            equipment_name="test_equipment",
            related_user=self.user_profile
        )

        self.test_date = datetime.date.today()
        self.unavailable_date = UnavailableDate.objects.create(
            date=self.test_date, related_user=self.user_profile
        )

    def test_userprofile_update(self):
        """
        Update User Profile model with all remaining data
        and confirm that it is saved and returned successfully.
        """

        user_profile = self.user_profile

        user_profile.first_name = "test_fname"
        user_profile.last_name = "test_lname"
        user_profile.city = "test_city"
        user_profile.country = "GB"
        user_profile.profile_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        user_profile.user_info = "test_user_info"

        user_profile.save()
        user_profile.instruments_played.add(self.instrument)
        user_profile.genres.add(self.genre)
        user_profile.save()
        self.assertTrue(self.user_profile.first_name, "test_fname")

    def test_userprofile_slug_creation(self):
        """
        Confirm that a representative slug is created upon
        creation of a user profile model.

        (User Profile model is created upon Auth User creation)
        """
        self.assertEqual(self.user_profile.slug, "test")

    def test_instrument_creation(self):
        """
        Retrieve instrument instance created in setUp method,
        and confirm that the instrument names match.
        """
        control_instrument = Instrument.objects.get(pk=1)
        self.assertEqual(control_instrument.instrument_name, "test_instrument")
    
    def test_genre_creation(self):
        """
        Retrieve genre instance created in setUp method,
        and confirm that the genre names match.
        """
        control_genre = Genre.objects.get(pk=1)
        self.assertEqual(control_genre.genre_name, "test_genre")

    def test_audiofile_filename_creation(self):
        """
        Create a dummy audiofile instance.

        Test "get_filename()" method of AudioFile model and confirm
        the method returns the correct filename.
        """
        test_file = tempfile.NamedTemporaryFile(suffix=".mp3").name

        new_audiofile = AudioFile.objects.create(
            file = test_file,
            related_user = self.user_profile
        )

        test_file_endpoint = "".join(test_file.split("/")[-1:])

        self.assertEquals(new_audiofile.file_name, test_file_endpoint)
    
    def test_unavailable_date_creation(self):
        """
        Unavailable date created in setUp method.
        Confirm that the created unavailable date matches the control
        date (today).
        """

        users_unavailable_date = self.user_profile.unavailable_user.get(date=self.test_date)
        self.assertEqual(self.test_date, users_unavailable_date.date)
        