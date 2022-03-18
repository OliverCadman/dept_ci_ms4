from django.urls import path
from .views import (create_checkout_session, SubscriptionChoiceView,
                    CheckoutSuccessView, CheckoutCancelledView, 
                    get_stripe_public_key, webhook, customer_portal)

urlpatterns = [
    path("choose_subscription/", SubscriptionChoiceView.as_view(), name="choose_subscription"),
    path("config/", get_stripe_public_key, name="config"),
    path("checkout/", create_checkout_session, name="checkout"),
    path("wh/", webhook, name="webhook"),
    path("success/", CheckoutSuccessView.as_view(), name="checkout_success"),
    path("cancelled/", CheckoutCancelledView.as_view(), name="checkout_cancelled"),
    path("customer_portal", customer_portal, name="customer_portal")
]