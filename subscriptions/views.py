from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from django.conf import settings

import os
if os.path.exists("env.py"):
    import env


class SubscriptionChoiceView(View):
    def get(self, request):

        tier_one_price = settings.TIER_ONE_PRICE
        tier_two_price = settings.TIER_TWO_PRICE

        context = {
            "tier_one_price": tier_one_price,
            "tier_two_price": tier_two_price
        }

        return render(request, "subscriptions/subscription_choices.html",
                      context=context)


@csrf_exempt
def create_checkout_session(request):
    if request.POST:
        print(request.POST["priceId"])
    
    tier_one_price_id = os.environ.get("STRIPE_TIERONE_PRICE_ID")
    tier_two_price_id = os.environ.get("STRIPE_TIERTWO_PRICE_ID")

    context = {
        "tier_one_price_id": tier_one_price_id,
        "tier_two_price_id": tier_two_price_id
    }
    
    return render(request, "subscriptions/checkout.html", context=context)


