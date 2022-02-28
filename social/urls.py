from django.urls import path

from .views import send_message


urlpatterns = [
    path("send_message/<str:message_receiver>/<int:invitation_id>", send_message, name="send_message")
]