from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from allauth.account.decorators import login_required
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.utils.safestring import mark_safe

from profiles.models import UserProfile
from social.functions import reverse_querystring

from .webhook_handler import StripeWH_Handler

import stripe
import json



class SubscriptionChoiceView(View):
    """
    View to display the two-tier subscription
    options to the user.
    """
    def get(self, request):
        
        # Redirect unauthenticated user to login if attempts to visit page manually
        if not self.request.user.is_authenticated:
          messages.info(self.request, "You need to login to subscribe.")
          return redirect(reverse_querystring("account_login", query_kwargs={
            "next": self.request.path
          }))


        current_user = get_object_or_404(UserProfile, user__username=request.user)

        tier_one_price = settings.TIER_ONE_PRICE
        tier_two_price = settings.TIER_TWO_PRICE

        tier_one_price_id = settings.STRIPE_TIERONE_PRICE_ID
        tier_two_price_id = settings.STRIPE_TIERTWO_PRICE_ID
        

        context = {
            "tier_one_price": tier_one_price,
            "tier_two_price": tier_two_price,
            "tier_one_price_id": tier_one_price_id,
            "tier_two_price_id": tier_two_price_id,
            "page_name": "choose_subscription",
            "current_user": current_user
        }
       

        return render(request, "subscriptions/subscription_choices.html",
                      context=context)

@csrf_exempt
def get_stripe_public_key(request):
    """
    Returns the Stripe public key to be handled in
    'js/checkout.js'
    """
    if request.method == "GET":
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        return JsonResponse({"public_key": stripe_public_key})

@login_required
@csrf_exempt
def create_checkout_session(request):
    """
    Creates a Stripe checkout session, handling either Tier One
    or Tier Two subscription events being sent from checkout.js"

    Returns the session id to be passed as an argument to in the
    URL upon redirection to Stripe's dedicated paymentz
    """
    if request.method == "POST":

        current_user = UserProfile.objects.get(user=request.user)
        price_id = request.POST["price_id"]

      
        if not current_user.is_paid:
            DOMAIN_ROOT = settings.DOMAIN_ROOT
            success_url = DOMAIN_ROOT + "subscribe/success?session_id="
            cancel_url = DOMAIN_ROOT + "subscribe/cancelled"
            stripe.api_key = settings.STRIPE_SECRET_KEY
            print("STRIPE API KEY")
            print(stripe.api_key)

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=success_url + "{CHECKOUT_SESSION_ID}",
                cancel_url = cancel_url,
                mode="subscription",
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1
                }],
                customer_email = current_user.user.email,
                metadata={
                    "customer_username": request.user.username
                }
            )

            print("CHECKOUT SESSION")
            print(checkout_session)

            request.session["CHECKOUT"] = True
            return JsonResponse({"session_id": checkout_session["id"]})
        
        except stripe.error.CardError as e:
            print(e)

@require_POST
def customer_portal(request):
  """
  Redirects the user to their personal Stripe portal,
  to manage their subscription.

  Creates a Stripe billing portal session, with the
  current user's Stripe Customer ID, and return URL
  redirecting the user to their dashboard.
  """
  
  if request.method == "POST":
    current_user = get_object_or_404(UserProfile, user__username=request.user)
    user_email = current_user.user.email
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Grab current user's Stripe 'Customer' account details
    # to get their ID, to be passed into stripe portal session.
    customer = stripe.Customer.list(email=user_email)

    if customer is not None:
        customer_id = customer.data[0].id
        try:
          session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=f"{settings.DOMAIN_ROOT}profile/dashboard/{current_user.slug}"
          )
          messages.info(request, "Redirect to Stripe portal")
          return redirect(session.url)
        except Exception as e:
          messages.error(request, "Sorry, something went wrong. Please try again.")
          return redirect(request.path)
    else:
      messages.error(request, "Sorry, we couldn't find you in our records.")
      return redirect(request.path)

    
  
@require_POST
@csrf_exempt
def webhook(request):
  payload = request.body
  sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
  event = None

  stripe.api_key = settings.STRIPE_SECRET_KEY
  stripe_wh_secret = settings.STRIPE_WH_SECRET

  try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, stripe_wh_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  handler = StripeWH_Handler(request)

  event_map = {
      'customer.subscription.created': handler.handle_customer_subscription_created,
      'customer.subscription.updated': handler.handle_customer_subscription_updated,
      'checkout.session.completed': handler.handle_checkout_completed,
      'charge.succeeded': handler.handle_payment_intent_succeeded,
      'payment_intent.payment_failed': handler.handle_payment_intent_failed,
      'invoice.created': handler.handle_invoice_created,
      'invoice.payment_action_required': handler.handle_invoice_requires_action,
      'invoice.upcoming': handler.handle_invoice_upcoming,
  }

  event_type = event['type']
  event_handler = event_map.get(event_type, handler.handle_event)

  response = event_handler(event)

  return response


# @csrf_exempt
# def webhook(request):
#     """
#     Listens for webhooks from Stripe
#     """

#     stripe_api_key = settings.STRIPE_SECRET_KEY
#     stripe_wh_secret = settings.STRIPE_WH_SECRET

#     event = None
#     payload = request.data
#     sig_header = request.headers['STRIPE_SIGNATURE']

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, stripe_wh_secret
#         )
#         print(event)
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(e, status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(e, status=400)
#     except Exception as e:
#         return HttpResponse(e, status=400)

#     # Handle the event
#     print('Unhandled event type {}'.format(event['type']))

#     print('Success')
#     return HttpResponse(status=200)

        
class CheckoutSuccessView(TemplateView):
    """
    View to inform user that the payment and subscription
    is successful.
    """

    template_name = "subscriptions/success.html"
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["page_name"] = "checkout_success"
      return context
  
 


class CheckoutCancelledView(View):
    """
    View to inform user that the checkout session has been
    cancelled.
    """
    def get(self, request):
        print(request)
        return render(request, "subscriptions/cancel.html")

        



