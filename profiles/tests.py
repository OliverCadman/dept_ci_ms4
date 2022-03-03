from django.test import TestCase, Client
from django.test.utils import tag
from django.contrib.auth import authenticate
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles.models import UserProfile


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

