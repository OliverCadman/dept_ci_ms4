from django.urls import path

from .views import send_message, get_notification_date, invitation_received_notification

urlpatterns = [
    path("send_message/<str:message_receiver>/<int:invitation_id>", send_message, name="send_message"),
    path("invite_received_notification/<int:notification_id>/<int:invitation_id>",
         invitation_received_notification, name="invite_received_notification"),
    path("get_notification_date", get_notification_date),
]