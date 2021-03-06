from django.urls import path
from .views import (invitation_form_view, get_invitation_messages,
                    accept_invitation, decline_invitation, booking_form,
                    BookingSuccessView, BookingDetailView, GeneratePDFFile,
                    download_audiofile, get_invitation_id,
                    tier_two_booking_form, EditInvitationForm,
                    delete_invitation)

"""
Booking URLS
--------------------

Routing for the Bookings App
"""

urlpatterns = [
    path('invite', invitation_form_view, name="invitation"),
    path("edit_invitation/<int:invitation_id>",
         EditInvitationForm.as_view(), name="edit_invitation"),
    path("delete_invitation/<int:invitation_id>",
         delete_invitation, name="delete_invitation"),
    path("get_invitation_messages/<int:pk>",
         get_invitation_messages, name="get_invitation_messages"),
    path("accept_invitation/<int:invitation_pk>",
         accept_invitation, name="accept_invitation"),
    path("decline_invitation/<int:invitation_pk>",
         decline_invitation, name="decline_invitation"),
    path("finalize_booking/<int:invitation_pk>",
         booking_form, name="booking_form"),
    path("finalize_tiertwo_booking/<int:job_id>",
         tier_two_booking_form, name="tier_two_booking_form"),
    path("success/<int:booking_id>",
         BookingSuccessView.as_view(), name="booking_success"),
    path("booking_detail/<int:pk>",
         BookingDetailView.as_view(), name="booking_detail"),
    path("generate_pdf/<int:booking_id>",
         GeneratePDFFile.as_view(), name="generate_pdf"),
    path("download_audiofile/<int:file_id>",
         download_audiofile, name="download_audiofile"),
    path("get_invitation_id/<int:booking_id>", get_invitation_id)
]
