from django.urls import path

from bookings.models import Invitation
from .views import (invitation_form_view, get_invitation_messages,
                    accept_invitation, booking_form, BookingSuccessView)

urlpatterns = [
    path('invite', invitation_form_view, name="invitation"),
    path("get_invitation_messages/<int:pk>", get_invitation_messages, name="get_invitation_messages"),
    path("accept_invitation/<int:invitation_pk>", accept_invitation, name="accept_invitation"),
    path("finalize_booking/<int:invitation_pk>", booking_form, name="booking_form"),
    path("success", BookingSuccessView.as_view(), name="booking_success")
]