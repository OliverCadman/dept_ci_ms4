from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile

import stripe


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic webhook event
        """

        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200
        )

    def handle_checkout_completed(self, event):
        """
        Listen for webhook "checkout.session.completed"
        and update the UserProfile model:

        - A subscription has been chosen (and)
        - The user has chosen the paid subscription
        """

        intent = event.data.object
        print("INTENT")
        print(intent)
        subscribed_username = intent.metadata.customer_username
     
        user_model = get_user_model()
        subscribing_user = user_model.objects.get(username=subscribed_username)
  
        user_profile = UserProfile.objects.get(user=subscribing_user)

        if intent.mode == "subscription":
            # Update UserModel with chosen subscription
            user_profile.subscription_chosen = True
            user_profile.save()

            # Get the subscription object and check if it is paid
            subscription_id = intent.subscription
            tier_two_price_id = settings.STRIPE_TIERTWO_PRICE_ID

            subscription = stripe.Subscription.retrieve(subscription_id)
            print("Retrieved subscription:", subscription)

            print('Subscription price id:', subscription["items"].data[0].price.id)

            # Update UserProfile model with paid-subscription-status
            if subscription["items"].data[0].price.id == tier_two_price_id:
                user_profile.is_paid = True
                user_profile.save()
                
        return HttpResponse(
            content=f"Checkout completed: {event['type']}"
        )

    def handle_customer_subscription_created(self, event):

        return HttpResponse(
            content=f"Subscription schedule created: {event['type']}",
            status=200
        )

    def handle_customer_subscription_updated(self, event):
        """
        Update the user's subscription status when they
        update their subscription through the Stripe customer
        portal.

        Grab the Price IDs from the event object and
        compare them with the Price IDs stored in
        variables in settings.py. 

        Revoke 'is_paid' status if Tier One Price ID matches,
        or add 'is_paid' status if Tier Two Price ID matches.
        """

        subscription = event.data.object 
        stripe_customer_id = subscription["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        customer_email = stripe_customer.email
        customer_profile = get_object_or_404(UserProfile, user__email=customer_email)

        subscription_price_id = subscription["items"].data[0].price.id

        tier_one_price_id = settings.STRIPE_TIERONE_PRICE_ID

        if subscription_price_id == tier_one_price_id:
            customer_profile.is_paid = False
            customer_profile.save()
        else:
            customer_profile.is_paid = True
            customer_profile.save()

        return HttpResponse(
            content=f"Subscription schedule updated: {event['type']}",
            status=200
        )

    

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook
        """

        intent = event.data.object
        # print("intent:", intent)

        return HttpResponse(
            content=f"Payment intent succeeded, nice one: {event['type']}",
            status=200
        )

    def handle_payment_intent_failed(self, event):
        return HttpResponse(
            content=f"Payment intent failed: {event['type']}"
        )

    def handle_invoice_requires_action(self, event):

        return HttpResponse(
            content=f"Action needed: {event['type']}"
        )

    def handle_invoice_upcoming(self, event):

        return HttpResponse(
            content=f"Invoice upcoming: {event['type']}"
        )
    
   

    def handle_invoice_created(self, event):

        return HttpResponse(
            content=f"Invoice created: {event['type']}",
            status=200
        )
