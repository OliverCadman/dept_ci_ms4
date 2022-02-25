
from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import DetailView


from datetime import datetime
from dateutil import parser

from .forms import InvitationForm
from profiles.models import UserProfile
from .models import Invitation

# Create your views here.

def invitation_form_view(request):

    invite_receiver_username = request.session.get("invited_username")
    invite_receiver = get_object_or_404(UserProfile, user__username=invite_receiver_username)
    invite_sender = get_object_or_404(UserProfile, user__username=request.user)

    if request.POST:
        event_datetime = request.POST.get("event_datetime")
        parsed_datetime = parser.parse(event_datetime)
    
        invitation_post = {
            "event_name": request.POST.get("event_name"),
            "artist_name": request.POST.get("artist_name"),
            "event_city": request.POST.get("event_city"),
            "event_country": request.POST.get("event_country"),
            "event_datetime": parsed_datetime,
            "fee": request.POST.get("fee"),
            "additional_info": request.POST.get("additional_info")
        }
        invitation_form = InvitationForm(invitation_post)

        if invitation_form.is_valid():
            try:
                form = invitation_form.save(commit=False)
                form.invite_sender = invite_sender
                form.invite_receiver = invite_receiver
                form.save()
                print("success")
                messages.success(request, "Invitation Sent")
            except Exception as e:
                print(f"Exception: {e}")
        else:
            if "event_datetime" in invitation_form.errors:
                messages.error(request, "Invalid date/time, please try again.")
            invitation_form = InvitationForm(request.POST, instance=request.user)

        return redirect(reverse("profile", kwargs={"user_name": invite_receiver}))


class InvitationDetailView(DetailView):

    model = Invitation

    