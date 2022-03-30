from django.test import TestCase
from django.urls import reverse, resolve
from home.views import IndexView


class TestHomeUrls(TestCase):
    """
    Unit Test Home URL

    Confirm the Home URL resolves correctly.
    """

    def test_home_url_is_resolved(self):
        url = reverse("home")
        self.assertEquals(
            resolve(url).func.__name__, IndexView.as_view().__name__
        )
