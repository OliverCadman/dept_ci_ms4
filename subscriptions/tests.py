from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

import urllib.parse

from profiles.models import UserProfile

from social.functions import reverse_querystring

"""
Subscription App - Testing

Test cases for Subscription Routes, Views and Config

- Test Subscription Choice Renders the Correct Page
- Test Stripe Price IDs in subscription choice context.
- Test Stripe config AJAX request returns Stripe Public Key.
- Test SessionId is returned in JSON in checkout view.
- Test redirect to login page if user is not authenticated.
- Test Success View is rendered after successful subscription
- Test Checkout Cancelled View redirects user to home page.
- Test redirect to home page if already-subscribed
  user visits success page.
"""


class TestSubscriptionApp(TestCase):
    
    def setUp(self):
        """
        Create a mock user and log them in.
        """
        username = "testuser"
        password = "abcde12345"
        email = "test@test.com"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username=username,
                                           password=password,
                                           email=email
                                        )
        login = self.client.login(username=username, password=password)
        self.assertTrue(login)

    def test_subscription_choice_view(self):
        """
        Confirm correct URL routing, and correct template is used.
        """
        response = self.client.get("/subscribe/choose_subscription/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("subscriptions/subscription_choices.html")

    def test_stripe_priceIDs_in_subscription_choice_context(self):
        """
        Confirm both Stripe Price IDs are present subscription-choice-view.
        context.
        """
        response = self.client.get("/subscribe/choose_subscription/")
        self.assertEquals(response.context["tier_one_price_id"],
                          settings.STRIPE_TIERONE_PRICE_ID)
        self.assertEquals(response.context["tier_two_price_id"],
                          settings.STRIPE_TIERTWO_PRICE_ID)

    def test_config_returns_stripe_pk(self):
        """
        Confirm that the AJAX GET request returns the
        Stripe Public Key.
        """
        response = self.client.get("/subscribe/config/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             { "public_key" : settings.STRIPE_PUBLIC_KEY })

    def test_session_id_in_checkout(self):
        """
        Confirm that the post request creates a checkout
        session ID.
        """
        tier_one_price_id = settings.STRIPE_TIERONE_PRICE_ID
        request_post_data = {
            "price_id": tier_one_price_id
        }
        response = self.client.post("/subscribe/checkout/", request_post_data)
        self.assertTrue("session_id" in response.json())

    def test_redirect_if_not_authenticated(self):
        """
        Confirm that an unauthenticated client is re-directed to login page
        if they attempt to visit the subscription choice page.
        """
        self.client.logout()
        response = self.client.get("/subscribe/choose_subscription/", follow=True)

        request_path_url = "/subscribe/choose_subscription/"
        self.assertRedirects(response, reverse_querystring("account_login",
                             query_kwargs={ "next" : urllib.parse.quote(request_path_url) }),
                             status_code=302, target_status_code=200)

    def test_checkout_success_view(self):
        """
        Confirm that the checkout success routing is correct, and 
        that the correct template is used.
        """
        self.client.get("/subscribe/choose_subscription")

        tier_one_price_id = settings.STRIPE_TIERONE_PRICE_ID
        request_post_data = {
            "price_id": tier_one_price_id
        }
        self.client.post("/subscribe/checkout/", request_post_data)
        session = self.client.session
        session["CHECKOUT"] = True
        session.save()

        response = self.client.get("/subscribe/success/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/subscriptions/success.html")

    def test_checkout_cancelled_redirect(self):
        """
        Confirm that a cancelled checkout session returns
        the user to the home page.
        """
        cancel_url = settings.DOMAIN_ROOT
        
        tier_one_price_id = settings.STRIPE_TIERONE_PRICE_ID
        request_post_data = {
            "price_id": tier_one_price_id
        }

        self.client.post("/subscribe/checkout/", request_post_data)
        response = self.client.get(cancel_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("home/index.html")

    def test_success_redirect_if_no_checkout_token(self):
        """
        Confirm that an already-subscribed user is redirected
        if they attempt to visit the checkout success page without
        a "CHECKOUT" session token.
        """
        user_profile = get_object_or_404(UserProfile, user__username=self.user)
        user_profile.subscription_chosen = True
        user_profile.save()
        response = self.client.get("/subscribe/success/", follow=True)
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)
