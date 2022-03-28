from django.urls import path

from .views import (send_message, invitation_received_notification,
                    invitation_accepted_notification,
                    booking_details_sent_notification,
                    remove_notification)
"""
Social - URLS

Define URL routing for Socials app.
"""
urlpatterns = [
     path("send_message/<str:message_receiver>/<int:invitation_id>",
          send_message,
          name="send_message"),

     path("invite_received_notification/"
          "<int:notification_id>/<int:invitation_id>",
          invitation_received_notification,
          name="invite_received_notification"),

     path("invite_accepted_notification/"
          "<int:notification_id>/<int:invitation_id>",
          invitation_accepted_notification,

          name="invite_accepted_notification"),
     path("booking_details_sent_notification/"
          "<int:notification_id>/<int:booking_id>",

          booking_details_sent_notification,
          name="booking_details_sent_notification"),

     path("remove_notification/<int:notification_id>",
          remove_notification,
          name="remove_notification"),
]
