
from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import View
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from datetime import datetime
from dateutil import parser

from .forms import InvitationForm, BookingForm
from profiles.models import UserProfile
from .models import Invitation
from social.models import Message

from .functions import to_dict
from social.functions import reverse_querystring

# Create your views here.

def invitation_form_view(request):
    """
    Form view rendered in User Profile modal, upon clicking
    'Contact <user>'
    """

    invite_receiver_username = request.session.get("invited_username")
    invite_receiver = get_object_or_404(UserProfile, user__username=invite_receiver_username)
    invite_sender = get_object_or_404(UserProfile, user__username=request.user)

    if request.POST:
        event_datetime = request.POST.get("event_datetime")
        # Parse the event_datetime value of request.POST to be interpreted by Python Django.
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


def get_invitation_messages(request, pk):
        """
        AJAX Handler to return all messages for a given
        invitation, to be displayed in modals triggered 
        from invitation cards.

        Additionally, all message objects for the given invitation
        are updated with 'is_read' status, and saved to the database.
        """
        invitation = get_object_or_404(Invitation, pk=pk)

        messages = invitation.invitation_messages.all()
        message_list = []

        if not len(messages) == 0:
            for message in messages:
                
                message_object = get_object_or_404(Message, pk=message.pk)
                message_object.is_read = True
                message_object.save()
                
                message = to_dict(message)
                print(message)
                message_list.append(message)
        else:
            print("NO MESSAGES")
        
        # Return JSON to be handled in JS file
        return JsonResponse({ "messages": message_list})


def accept_invitation(request, invitation_pk):
    """
    Updates relevant Invitation object with 'accepted' status,
    and sends the invite receiver a confirmation email upon 
    once the Invitation object has been updated and saved successfully.
    """

    invitation = get_object_or_404(Invitation, pk=invitation_pk)

    invite_receiver = get_object_or_404(UserProfile, user__username=request.user)
    invite_sender = get_object_or_404(UserProfile, user__username=invitation.invite_sender)

    try:
        invitation.is_accepted = True
        invitation.save()

        invitation_number = invitation.invitation_number

        # Send Confirmation Email to Invite Receiver
        invite_receiver_email = invite_receiver.user.email
        subject = render_to_string(
            'bookings/confirmation_emails/confirmation_email_subject.txt',
            { "invitation_number": invitation_number }
        )
        body = render_to_string(
            'bookings/confirmation_emails/confirmation_email_receiver_body.txt', 
            { "invitation": invitation }
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [invite_receiver_email]
        )
        
        # Send Email Confirmation to Invite Sender
        invite_sender_email = invite_sender.user.email
        subject = render_to_string(
            "bookings/confirmation_emails/confirmation_email_subject.txt",
            { "invitation_number": invitation_number }
        )
        body = render_to_string(
            "bookings/confirmation_emails/confirmation_email_sender_body.txt",
            { "invitation": invitation }
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [invite_sender_email]
        )

        messages.success(request, "Great, your invitation has been accepted!")
        return redirect(reverse_querystring("dashboard", args=[invite_receiver.slug], query_kwargs={"page": "jobs"}))
    except Exception as e:
        print("Exception:", e)
        messages.error(request, "Sorry something went wrong. Please try again")
        return redirect(reverse_querystring("dashboard", args=[invite_receiver.slug], query_kwargs={ "page": "jobs" }))


class BookingFormView(View):

    def get(self, request, invitation_pk):

        current_invitation = get_object_or_404(Invitation, pk=invitation_pk)
        invitation_form = InvitationForm(instance=current_invitation)
        booking_form = BookingForm()

        context = {
            "invitation_form": invitation_form,
            "booking_form": booking_form
        }

        return render(request, "bookings/booking_form.html", context=context)

   