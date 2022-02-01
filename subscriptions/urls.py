from django.urls import path
from .views import create_checkout_session, SubscriptionChoiceView

urlpatterns = [
    path('', create_checkout_session, name="checkout"),
    path('choose_subscription', SubscriptionChoiceView.as_view(), name="subscription_choices")
]