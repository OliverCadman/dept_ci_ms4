from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from profiles.models import UserProfile

# Create your tests here.

class TestHomePage(TestCase):
    """
    Test Class for Home Page View.
    """

    def test_get_home_page(self):
        """
        Check that the home page url resolves with
        success status code and template.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
    

    def test_get_home_page_by_name(self):
        """
        Check that the reverse name for home page resolves
        with success status code and template.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")


class TestHomePageRedirect(TestCase):
    """
    Test for direct to subscription page if user hasn't
    chosen a subscription.
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
        self.client.login(username=username, password=password)

    
    def test_redirect_url_if_no_subscription_chosen(self):
        """
        Attempt to visit home page when user is logged in, and
        check if redirect url resolves with success status code,
        and correct template is used.
        """
        response = self.client.get("/", follow=True)
        self.assertRedirects(response, "/subscribe/choose_subscription/", status_code=302, 
                             target_status_code=200)
        self.assertTemplateUsed(response, "subscriptions/subscription_choices.html")

    
    def test_redirect_reverse_if_no_subscription_chosen(self):
        """
        Attempt to visit home page when user is logged in, and
        check if redirect reverse resolves with success status code,
        and correct template is used.
        """
        response = self.client.get("/", follow=True)
        self.assertRedirects(response, reverse("choose_subscription"), status_code=302, 
                             target_status_code=200)
        self.assertTemplateUsed(response, "subscriptions/subscription_choices.html")
