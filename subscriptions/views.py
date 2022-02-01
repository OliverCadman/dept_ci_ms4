from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import os
if os.path.exists("env.py"):
    import env


class SubscriptionChoiceView(View):
    def get(self, request):
        return render(request, "subscriptions/subscription_choices.html")


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


