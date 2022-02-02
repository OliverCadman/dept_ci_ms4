from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.conf import settings

from profiles.models import UserProfile

import stripe



class SubscriptionChoiceView(View):
    """
    Handles the view displaying subscription options.
    """
    def get(self, request):

        tier_one_price = settings.TIER_ONE_PRICE
        tier_two_price = settings.TIER_TWO_PRICE

        tier_one_price_id = settings.STRIPE_TIERONE_PRICE_ID
        tier_two_price_id = settings.STRIPE_TIERTWO_PRICE_ID
        

        context = {
            "tier_one_price": tier_one_price,
            "tier_two_price": tier_two_price,
            "tier_one_price_id": tier_one_price_id,
            "tier_two_price_id": tier_two_price_id
        }

        return render(request, "subscriptions/subscription_choices.html",
                      context=context)

@csrf_exempt
def get_stripe_public_key(request):
    """
    Returns the stripe public key to be handled in 'js/checkout.js'
    to allow for redirect to Stripe checkout.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    return JsonResponse({"public_key": stripe_public_key})
                      

@csrf_exempt
def create_checkout_session(request):
    """
    Creates a Stripe checkout session, handling either Tier One
    or Tier Two subscription events being sent from checkout.js"

    Returns the session id to be passed as an argument to in the
    URL upon redirection to Stripe's dedicated payment portal.
    """
    if request.method == "POST":

        current_user = UserProfile.objects.get(user=request.user)
        price_id = request.POST["price_id"]
        print(price_id)

        if not current_user.is_paid:
            DOMAIN_ROOT = settings.DOMAIN_ROOT
            success_url = DOMAIN_ROOT + "subscribe/success?session_id="
            cancel_url = DOMAIN_ROOT + "subscribe/cancelled"
            stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=success_url + "{CHECKOUT_SESSION_ID}",
                cancel_url = cancel_url,
                mode="subscription",
                payment_method_types=["card"],
                line_items=[{
                    'price': price_id,
                    'quantity': 1
                }]
            )

            return JsonResponse({"session_id": checkout_session["id"]})
        
        except stripe.error.CardError as e:
            print(e)




