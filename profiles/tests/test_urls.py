from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


from profiles.views import (ProfileView, delete_account, edit_profile, upload_audio,
                    upload_unavailable_dates, get_users_unavailable_dates,
                    get_users_tracks, DashboardView, delete_account)
from profiles.models import UserProfile

from social.functions import reverse_querystring


class TestProfileUrls(TestCase):
    """
    Unit Tests - Profile URLs

    Ensures that the routing to every URL in the profile
    app resolves correctly.
    """

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
            UserProfile,user=self.user)

    def test_profile_url_is_resolved(self):
        """
        Confirm that the Profile URL resolves correctly.
        """
        url = reverse("profile", args=[self.user])
        self.assertEquals(resolve(url).func.__name__, ProfileView.as_view().__name__)

    def test_delete_account_url_is_resolved(self):
        """
        Confirm that the Delete Account URL resolves correctly.
        """
        url = reverse("delete_account", args=[self.user_profile.pk])
        self.assertEquals(resolve(url).func, delete_account)

    def test_edit_profile_url_is_resolved(self):
        """
        Confirm that the Edit Profile URL resolves correctly.
        """
        url = reverse("edit_profile")
        self.assertEquals(resolve(url).func, edit_profile)

    def test_upload_audio_url_is_resolved(self):
        """
        Confirm that the Upload Audio URL resolves correctly.
        """
        url = reverse("upload_audio", args=[self.user])
        self.assertEquals(resolve(url).func, upload_audio)

    def test_upload_unavailable_dates_url_is_resolved(self):
        """
        Confirm that the upload_unavailable_dates URL resolves correctly.
        """
        url = reverse("upload_unavailability", args=[self.user.pk])
        self.assertEquals(resolve(url).func, upload_unavailable_dates)

    def test_get_users_unavailable_dates_url_is_resolved(self):
        """
        Confirm that the get_users_unavailable_dates URL resolves correctly.
        """
        url = reverse("get_users_unavailable_dates", args=[self.user.pk])
        self.assertEquals(resolve(url).func, get_users_unavailable_dates)

    def test_get_users_tracks_url_is_resolved(self):
        """
        Confirm that the get_users_tracks URL resolves correctly.
        """
        url = reverse("get_users_tracks", args=[self.user.pk])
        self.assertEquals(resolve(url).func, get_users_tracks)

    def test_dashboard_url_is_resolved(self):
        """
        Confirm that the Dashboard URL resolves correctly.
        """
        url = reverse("dashboard", args=[self.user_profile.slug])
        self.assertEquals(resolve(url).func.__name__, DashboardView.as_view().__name__)

    
