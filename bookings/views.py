from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.forms.models import modelformset_factory
from django.views.generic import View, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.template.loader import get_template

from dateutil import parser

from .forms import InvitationForm, BookingForm
from .models import Invitation, Booking
from .functions import to_dict
from .utils import render_to_pdf


from social.models import Message
from social.functions import reverse_querystring
from profiles.forms import AudioForm
from profiles.models import UserProfile, AudioFile


def invitation_form_view(request):
    """
    Form view rendered in User Profile modal, upon clicking
    'Contact <user>'
    """

    invite_receiver_username = request.session.get("invited_username")
    invite_receiver = get_object_or_404(UserProfile,
                                        user__username=invite_receiver_username)
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

    invite_receiver = get_object_or_404(UserProfile,
                                        user__username=request.user)
    invite_sender = get_object_or_404(UserProfile,
                                      user__username=invitation.invite_sender)

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
        return redirect(reverse_querystring("dashboard",
                                            args=[invite_receiver.slug],
                                            query_kwargs={"page": "jobs"}))
    except Exception as e:
        print("Exception:", e)
        messages.error(request, "Sorry something went wrong. Please try again")
        return redirect(reverse_querystring("dashboard",
                                            args=[invite_receiver.slug],
                                            query_kwargs={ "page": "jobs" }))

@login_required
def booking_form(request, invitation_pk):
    """
    Booking Form Page

    Displays and handles all form data related to a particular booking/invitation.
    Contains two forms:

    - Booking Form
    - AudioFormset Factory

    AudioFormsetFactory provides dynamic addition of audio form file fields.
    """

    current_invitation = get_object_or_404(Invitation, pk=invitation_pk)


    current_booking = get_object_or_404(Booking, related_invitation=current_invitation)
    

    invitation_form = InvitationForm(instance=current_invitation)
    booking_form = BookingForm()

    # Initialize formset factory and query booking object for audio files
    AudioFormsetFactory = modelformset_factory(AudioFile, form=AudioForm, extra=1)
    queryset = current_booking.audio_resources.all()
    audio_formset = AudioFormsetFactory(request.POST or None, request.FILES or None,
                                        queryset=queryset)

    if request.method == "POST":
        booking_form = BookingForm(request.POST or None, instance=current_booking)
        audio_formset = AudioFormsetFactory(request.POST or None, request.FILES or None,
                                            queryset=queryset)

        if all([booking_form.is_valid(), audio_formset.is_valid()]):
            # Process Booking Form
            parent_form = booking_form.save(commit=False)
            parent_form.save()
            for form in audio_formset:
                child_form = form.save(commit=False)
                # Assign Audio Formset to related booking (if not done so already)
                if child_form.related_booking is None:
                    child_form.related_booking = parent_form
                child_form.save()

            request.session["booking_id"] = (
                current_booking.related_invitation.invitation_number)

            messages.success(request, "Booking Form Submitted")
            return redirect(reverse("booking_success", args=[current_booking.id]))
        else:
            messages.error(request, "Your form was invalid, please try again.")

    context = {
        "invitation_form": invitation_form,
        "booking_form": booking_form,
        "audio_formset": audio_formset,
        "invitation": current_invitation,
        "page_name": "booking_form",
    }

    return render(request, "bookings/booking_form.html", context=context)


class BookingSuccessView(View):
    """
    Booking Success View

    Rendered after submitting finalized booking details.
    Displays complete booking information.
    """
    def get(self, request, booking_id):
        event = get_object_or_404(Booking, pk=booking_id)

        # Restricts access to page only to users associated with the booking.
        if (not event.related_invitation.invite_sender.user.username == request.user.username
            and not event.related_invitation.invite_receiver.user.username == request.user.username):
            messages.warning(request, mark_safe("You may not browse another user's booking."))
            return redirect(reverse("home"))

        context = {
            "page_name": "booking_success",
            "event": event,
        }

        return render(request, "bookings/booking_success.html",
                      context=context)


class BookingDetailView(DetailView):
    """
    View to display a single instance of a booking.
    """

    model = Booking

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["page_name"] = "booking_detail"
        
        return context
    
    def get(self, request, *args, **kwargs):
        template_name = "bookings/booking_detail.html"
        self.object = self.get_object()
        context = self.get_context_data(object=self.get_object())

        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user__username=user)
        booking_receiver = self.object.related_invitation.invite_receiver
        
        if user_profile != booking_receiver:
            messages.warning(self.request, mark_safe("You may not browse another user's booking."))
            return redirect(reverse("home"))

        return render(request, template_name=template_name, context=context)


class GeneratePDFFile(View):
    """
    View to display Booking Detail in downloadable PDF format.

    Methods:

    get() - Retrieves the booking id as args and gets booking.
          - Creates a context containing the booking and passes
            template and context into render_to_pdf().
          - If PDF is valid, returns a HTTPResponse containing
            the generated pdf along with relevant content type.
          - Download is taken from request if user clicks the
            browser-generated download button.

    https://www.codingforentrepreneurs.com/blog/html-template-to-pdf-in-django/
    """
    def get(self, request, *args, **kwargs):
        booking_id = self.kwargs["booking_id"]
        current_booking = get_object_or_404(Booking, pk=booking_id)

        # Get Booking Detail Display template using django template loaders
        template = get_template("bookings/pdf_files/booking_detail_display_pdf.html")

        # Define the context (current booking)
        context = {
            "event": current_booking
        }

        html = template.render(context)

        # Invoke render_to_pdf to convert HTML into PDF format
        pdf = render_to_pdf("bookings/pdf_files/booking_detail_display_pdf.html", context)

        # Return HTTPResponse containing prepared PDF
        # String format filename to include specific booking number in case of download.
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Booking %s.pdf" %(current_booking.related_invitation.invitation_number)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)

            # Inform the browser that the response should be treated as an attachment
            response["Content-Disposition"] = content
            return response

        messages.error(self.request, "Sorry, the PDF couldn't be downloaded now. Please try again.")
        return redirect(reverse("booking_detail", args=[current_booking.pk]))
        
