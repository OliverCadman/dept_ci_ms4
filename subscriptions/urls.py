from django.urls import path
from .views import (create_checkout_session, SubscriptionChoiceView,
                    CheckoutSuccessView, CheckoutCancelledView, get_stripe_public_key)

urlpatterns = [
    path('choose_subscription', SubscriptionChoiceView.as_view(), name="subscription_choices"),
    path('checkout', create_checkout_session, name="checkout"),
    path("success", CheckoutSuccessView.as_view(), name="checkout_success"),
    path("cancelled", CheckoutCancelledView.as_view(), name="checkout_cancelled")
]