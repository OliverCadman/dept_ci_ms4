from django.urls import path

from bookings.models import Invitation
from .views import invitation_form_view, get_invitation_messages

urlpatterns = [
    path('invite', invitation_form_view, name="invitation"),
    path("get_invitation_messages/<int:pk>", get_invitation_messages, name="get_invitation_messages"),
]