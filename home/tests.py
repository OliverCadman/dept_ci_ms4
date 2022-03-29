from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from profiles.models import UserProfile


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
