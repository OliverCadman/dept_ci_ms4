from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import View

from .functions import reverse_querystring

from profiles.models import UserProfile
from bookings.models import Invitation

from .forms import MessageForm
from .models import Notification


def send_message(request, message_receiver, invitation_id):
    """
    Sends a message between members of the website who are involved
    in an active invitation/booking.
    """

    message_sender = get_object_or_404(UserProfile, user__username=request.user)

    message_receiver = get_object_or_404(UserProfile, user__username=message_receiver)

    invitation = get_object_or_404(Invitation, pk=invitation_id)

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.message_sender = message_sender
            message.message_receiver = message_receiver
            message.invitation_id = invitation
            message_form.save()
            messages.success(request, f"Message sent to {message_receiver}")
            return redirect(reverse_querystring("dashboard", args=[message_sender.slug], query_kwargs={'page': 'jobs'}))
        else:
            messages.error(request, "Sorry, message not sent. Please make sure your message is valid.")
            return redirect(reverse_querystring("dashboard", args=[message_sender.slug], query_kwargs={'page': 'jobs'}))

def get_notification_date(request):

    return JsonResponse({"hello": request.user.username})


def invitation_received_notification(request, notification_id, invitation_id):
    """
    View to handle "Invite Received" notification, when notification is clicked.

    Sets the 'is_read' field of related notification object to True, and 
    redirects user to their dashboard, displaying the specific invitation
    in question.
    """

    notification = get_object_or_404(Notification, pk=notification_id)
    notification.is_read = True
    notification.save()

    invitation = get_object_or_404(Invitation, pk=invitation_id)

    current_user = get_object_or_404(UserProfile, user__username=request.user)

    # Inject Invitation ID into session to be picked up in Dashboard View.
    request.session["invitation_id"] = invitation.pk

    return redirect(reverse_querystring("dashboard", args=[current_user.slug],
                                            query_kwargs={
                                                "page": "jobs",
                                                "section": "invites_received",
                                                "filter": invitation.pk
                                            }))


        
    
        
        

