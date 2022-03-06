from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

from .functions import reverse_querystring

from profiles.models import UserProfile
from bookings.models import Invitation
from .forms import MessageForm


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
