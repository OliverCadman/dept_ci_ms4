from django.urls import path

from bookings.models import Invitation
from .views import invitation_form_view, InvitationDetailView

urlpatterns = [
    path('invite', invitation_form_view, name="invitation"),
    path("invite/<int:pk>", InvitationDetailView.as_view(), name="invitation_detail")
]