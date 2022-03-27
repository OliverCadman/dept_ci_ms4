
import os


from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import (JsonResponse, HttpResponse,
                         HttpResponseRedirect)
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.forms.models import modelformset_factory
from django.views.generic import View, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.template.loader import get_template

from .forms import InvitationForm, BookingForm
from .models import Invitation, Booking
from .functions import to_dict
from .utils import render_to_pdf
from .classes import DownloadS3Object

from social.models import Message, Notification
from social.functions import reverse_querystring, get_referral_path
from profiles.forms import AudioForm
from profiles.models import UserProfile, AudioFile
from jobs.models import Job
from jobs.forms import JobForm

from dateutil import parser


def invitation_form_view(request):
    """
    Form view rendered in User Profile modal, upon clicking
    'Contact <user>'
    """

    invite_receiver_username = request.session.get("invited_username")
    invite_receiver = get_object_or_404(
        UserProfile, user__username=invite_receiver_username)
    invite_sender = get_object_or_404(
        UserProfile, user__username=request.user)

    if request.POST:
        event_datetime = request.POST.get("event_datetime")
        # Parse the event_datetime value of request.POST
        # to be interpreted by Python Django.
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
            form = invitation_form.save(commit=False)
            form.invite_sender = invite_sender
            form.invite_receiver = invite_receiver
            form.save()

            messages.success(request, "Invitation Sent")
            return redirect(
                reverse("profile", kwargs={"user_name": invite_receiver}))
        else:
            return JsonResponse({"errors": invitation_form.errors.as_json()})


class EditInvitationForm(UpdateView):
    """
    Updates a given Invitation object using InvitationForm,
    with fields pre-populated with values inputted by the
    invite sender from submitting the original form from
    a profile page.
    """
    template_name = "bookings/edit_invitation.html"
    form_class = InvitationForm

    # Make Django aware of which model needs to be queried.
    queryset = Invitation.objects.all()

    def get_object(self):
        """
        Get the current invitation
        """

        invitation_id = self.kwargs.get("invitation_id")
        return get_object_or_404(Invitation, pk=invitation_id)

    def get(self, *args, **kwargs):
        """
        Restrict access to page only to user who owns the
        Invitation object.
        """
        request_user_profile = get_object_or_404(
            UserProfile, user__username=self.request.user
            )

        invitation = self.get_object()

        if invitation.invite_sender != request_user_profile:
            messages.warning(
                self.request,
                mark_safe("You may not browse another user's invitation."))

            return redirect(reverse("home"))

        return super().get(*args, **kwargs)

    def form_valid(self, form):
        """
        Return success message upon successful submission of form.
        """

        messages.success(self.request, "Invitation form edited")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Process the "event_datetime" field of the post request,
        turning it into a python datetime object, interpretable
        by Django.
        """

        event_datetime = request.POST.get("event_datetime")
        parsed_datetime = parser.parse(event_datetime)
        request.POST = request.POST.copy()
        request.POST["event_datetime"] = parsed_datetime

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Get invitation object and use invitation sender's slug
        in query arg , along with the relevant page,
        section, subsection and invitation pk as filter keyword args.
        """

        invitation = self.get_object()
        invite_sender = invitation.invite_sender
        return reverse_querystring("dashboard",
                                   args=[invite_sender.slug],
                                   query_kwargs={
                                       "page": "jobs",
                                       "section": "tier_one",
                                       "subsection": "invites_sent",
                                       "filter": invitation.pk
                                   })


def get_invitation_messages(request, pk):
        """
        AJAX Handler to return all messages for a given
        invitation, to be displayed in modals triggered
        from invitation cards.

        Additionally, all message objects for the given invitation
        are updated with 'is_read' status, and saved to the database.
        """

        referal_path = get_referral_path(
            request, split_index1="/", split_index2="&",
            slice_index1=5, slice_index2=1)

        messages = None
        if not referal_path == "section=tier_two":

            invitation = get_object_or_404(Invitation, pk=pk)

            messages = invitation.invitation_messages.all()
        else:
            job = get_object_or_404(Job, pk=pk)

            messages = job.job_messages.all()
        message_list = []

        if not len(messages) == 0:
            for message in messages:

                message_object = get_object_or_404(
                    Message, pk=message.pk)
                message_object.is_read = True
                message_object.save()

                message = to_dict(message)
                message_list.append(message)

        # Return JSON to be handled in JS file
        return JsonResponse({"messages": message_list})


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
            {"invitation_number": invitation_number}
        )
        body = render_to_string(
            "bookings/confirmation_emails/"
            "confirmation_email_receiver_body.txt",
            {"invitation": invitation}
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
            {"invitation_number": invitation_number}
        )
        body = render_to_string(
            "bookings/confirmation_emails/"
            "confirmation_email_sender_body.txt",
            {"invitation": invitation}
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
        messages.error(request, "Sorry something went wrong. Please try again")
        return redirect(reverse_querystring("dashboard",
                                            args=[invite_receiver.slug],
                                            query_kwargs={"page": "jobs"}))


def decline_invitation(request, invitation_pk):
    """
    View to handle declined invitations.

    Gets the invitation object by ID and deletes from the database.

    If successful, success message displayed along with redirect
    to "Received Invites" section of Jobs page, on Dashboard page.

    If unsuccessful, error message displayed along with redirect to
    "Received Invites" section of Jobs page, on Dashboard page.
    """
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    invite_sender = get_object_or_404(
        UserProfile, pk=invitation.invite_sender.pk)

    invite_sender_name = None
    if invitation.invite_sender.first_name:
        invite_sender_name = invitation.invite_sender.first_name
    else:
        invite_sender_name = invitation.invite_sender.user.username

    try:
        invite_receiver = invitation.invite_receiver
        declined_invitation = invitation.event_name

        Notification.objects.create(
            notification_sender=invite_receiver,
            notification_receiver=invite_sender,
            notification_type=3,
            declined_invitation=declined_invitation
        )

        invitation.delete()
        messages.success(request, mark_safe(
            f"You declined {invite_sender_name}'s invitation."))
        return redirect(reverse_querystring("dashboard", args=[request.user],
                                            query_kwargs={
                                                "page": "jobs",
                                                "section": "invites_received",
                                                "filter": "all"
                                            }))
    except Exception as e:
        messages.error(
            request, "Sorry, something went wrong, please try again.")
        return redirect(
            reverse_querystring("dashboard", args=[request.user],
                                query_kwargs={
                                    "page": "jobs",
                                    "section": "invites_received",
                                    "filter": "all"
                                }))


def delete_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)
    invite_sender = invitation.invite_sender
    invite_receiver = invitation.invite_receiver
    try:
        Notification.objects.create(
            notification_sender=invite_sender,
            notification_receiver=invite_receiver,
            declined_invitation=invitation.event_name,
            notification_type=7
        )
        invitation.delete()
        messages.success(request, "Invitation deleted.")
        return redirect(reverse("dashboard", args=[invite_sender.slug]))
    except Exception as e:
        messages.error(request, f"Sorry, something went wrong: {e}")
        return redirect(reverse("dashboard", args=[invite_sender.slug]))


@login_required
def booking_form(request, invitation_pk):
    """
    Booking Form Page

    Displays and handles all form data related to a particular
    booking/invitation.

    Contains two forms:

    - Booking Form
    - AudioFormset Factory

    AudioFormsetFactory provides dynamic addition of
    audio form file fields.
    """

    current_user = get_object_or_404(
        UserProfile, user__username=request.user)

    current_invitation = get_object_or_404(
        Invitation, pk=invitation_pk)

    # Restrict access to page to user responsible for invite.
    if (current_invitation.invite_sender != current_user):
        messages.warning(request, mark_safe(
            "You may not browse another member's booking."))
        return redirect(reverse("home"))

    current_booking = get_object_or_404(
        Booking, related_invitation=current_invitation)

    invitation_form = InvitationForm(instance=current_invitation)
    booking_form = BookingForm(instance=current_booking)

    # Initialize formset factory and query booking object for audio files
    AudioFormsetFactory = modelformset_factory(
        AudioFile, form=AudioForm, extra=1)
    queryset = current_booking.audio_resources.all()
    audio_formset = AudioFormsetFactory(
        request.POST or None, request.FILES or None,
        queryset=queryset)

    # Post Booking Form and Audio Formset Factory
    if request.method == "POST":
        booking_form = BookingForm(
            request.POST or None, instance=current_booking)
        audio_formset = AudioFormsetFactory(
            request.POST or None, request.FILES or None,
            queryset=queryset)

        if all([booking_form.is_valid(), audio_formset.is_valid()]):
            # Process Booking Form
            parent_form = booking_form.save(commit=False)
            parent_form.save()

            try:
                current_booking.booking_details_sent = True
                current_booking.save()
            except Exception as e:
                print(f"Exception: {e}")
            # Process Audio Formset
            for form in audio_formset:
                child_form = form.save(commit=False)
                # Assign Audio Formset to related
                # booking (if not done so already)
                if child_form.related_booking is None:
                    child_form.related_booking = parent_form
                child_form.save()

            request.session["booking_id"] = (
                current_booking.related_invitation.invitation_number)

            request.session["tier_one_booking_form"] = True

            messages.success(request, "Booking Form Submitted.")
            return redirect(
                reverse("booking_success", args=[current_booking.id]))
        else:
            messages.error(
                request, "Your form was invalid, please try again.")
            return redirect(
                reverse("booking_form", args=[current_invitation.pk]))

    context = {
        "invitation_form": invitation_form,
        "booking_form": booking_form,
        "audio_formset": audio_formset,
        "invitation": current_invitation,
        "page_name": "booking_form",
    }

    return render(request, "bookings/booking_form.html", context=context)


@login_required
def tier_two_booking_form(request, job_id):
    """
    Tier Two Booking Form

    Displays and handles all form data related to a
    confirmed Job related to the Tier Two "Find a Job" service.
    Contains two forms:

    - Booking Form
    - AudioFormset Factory

    AudioFormsetFactory provides dynamic
    addition of audio form file fields.
    """

    current_job = get_object_or_404(Job, pk=job_id)
    current_user = get_object_or_404(
        UserProfile, user__username=request.user.username)

    # Restrict access to page to user responsible for invite.
    if (current_job.job_poster != current_user):
        messages.warning(request, mark_safe(
            "You may not browse another member's booking."))
        return redirect("home")

    current_booking = get_object_or_404(Booking, related_job=current_job)

    job_form = JobForm(instance=current_job)
    booking_form = BookingForm(instance=current_booking)

    # Initialize formset factory and query booking object for audio files
    AudioFormsetFactory = modelformset_factory(
        AudioFile, form=AudioForm, extra=1)
    queryset = current_booking.audio_resources.all().exclude(file="")
    audio_formset = AudioFormsetFactory(
        request.POST or None, request.FILES or None,
        queryset=queryset)

    if request.method == "POST":
        booking_form = BookingForm(
            request.POST or None, instance=current_booking)
        audio_formset = AudioFormsetFactory(
            request.POST or None, request.FILES or None,
            queryset=queryset)

        if all([booking_form.is_valid(), audio_formset.is_valid()]):
            # Process Booking Form
            parent_form = booking_form.save(commit=False)
            parent_form.save()

            try:
                current_booking.booking_details_sent = True
                current_booking.save()
            except Exception as e:
                print(f"Exception: {e}")

            for form in audio_formset:
                child_form = form.save(commit=False)
                # Assign Audio Formset to related
                # booking (if not done so already)
                if child_form.related_booking is None:
                    child_form.related_booking = parent_form
                child_form.save()

            request.session["tier_two_booking_form_submit"] = True

            messages.success(request, "Booking Form Submitted")
            return redirect(
                reverse("booking_success", args=[current_booking.id]))
        else:
            messages.error(request, "Your form was invalid, please try again.")
            return redirect(
                reverse("tier_two_booking_form", args=[current_job.pk]))

    context = {
        "job_form": job_form,
        "booking_form": booking_form,
        "audio_formset": audio_formset,
        "job": current_job,
        "page_name": "tier_two_booking_form",
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

        tier_type = None
        if not self.request.session.get("tier_two_booking_form_submit"):
            tier_type = 1

            invite_sender = event.related_invitation.invite_sender
            invite_receiver = event.related_invitation.invite_receiver

            # Restricts access to page only to users
            # associated with the booking.
            if (not invite_sender.user == request.user and not
                    invite_receiver == request.user):
                    messages.warning(
                        request, mark_safe(
                            "You may not browse another user's booking."))
                    return redirect(reverse("home"))
        else:
            tier_type = 2

        context = {
            "page_name": "booking_success",
            "event": event,
            "tier_type": tier_type
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

        booking_details_sent = self.object.booking_details_sent
        if not booking_receiver == user and not booking_details_sent:
            messages.info(request, mark_safe(
                "The booking details haven't been sent yet."))

            return redirect(
                reverse_querystring("dashboard", args=[user_profile.slug],
                                    query_kwargs={
                                        "page": "jobs",
                                        "section": "tier_one",
                                        "subsection": "invites_sent",
                                        "filter": "all"
                                    }))

        if user_profile != booking_receiver:
            messages.warning(self.request, mark_safe(
                "You may not browse another user's booking."))
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

        # Restrict access to view only to booking receiver.
        current_user = get_object_or_404(
            UserProfile, user__username=request.user)

        invite_receiver = (
            current_booking.related_invitation.invite_receiver)

        if current_user != invite_receiver:
            messages.warning(
                request, "You may not browse another user's booking.")
            return redirect(reverse("home"))

        # Get Booking Detail Display template using django template loaders
        template = get_template(
            "bookings/pdf_files/booking_detail_display_pdf.html")

        # Define the context (current booking)
        context = {
            "event": current_booking
        }

        html = template.render(context)

        # Invoke render_to_pdf to convert HTML into PDF format
        pdf = render_to_pdf(
            "bookings/pdf_files/booking_detail_display_pdf.html", context)

        # Return HTTPResponse containing prepared PDF
        # String format filename to include specific
        # booking number in case of download.
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Booking %s.pdf" % (
                current_booking.related_invitation.invitation_number)
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)

            # Inform the browser that the response shoulb
            # be treated as an attachment
            response["Content-Disposition"] = content
            return response

        messages.error(
            self.request,
            "Sorry, the PDF couldn't be downloaded now. Please try again.")

        return redirect(reverse("booking_detail", args=[current_booking.pk]))


def download_audiofile(request, file_id):
    """
    View to handle request to download audio files.

    Both a development method and production method are required
    since the serving the file from the production backend "Amazon S3"
    requires different configuration and methods to serving the
    file in development.
    """
    audio_file = get_object_or_404(AudioFile, pk=file_id)

    # ------------ DEVELOPMENT -----------------
    # If fsock is valid, return HTTP Response to serve the
    # prepared audio file, as audio/mpeg attachment.
    # https://stackoverflow.com/questions/2681338/
    # django-serving-a-download-in-a-generic-view

    if "DEVELOPMENT" in os.environ:
        fsock = open(audio_file.file.path, "rb")
        if fsock:
            response = HttpResponse(fsock, content_type="audio/mpeg")
            response["Content-Disposition"] = (
                "attachment; filename=%s" % (audio_file.file_name))

            return response

        booking_id = audio_file.related_booking.pk
        messages.error(
            request, "Sorry, something went wrong, please try again.")
        return redirect(reverse("booking_detail", args=[booking_id]))

    # ----------- PRODUCTION ----------
    else:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        access_key = settings.AWS_ACCESS_KEY_ID
        region = settings.AWS_S3_REGION_NAME
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        expiration = settings.AWS_DOWNLOAD_EXPIRE
        audio_filepath = audio_file.file.name

        # Instantiate the DownloadS3Object class and
        # call generate_download_url
        audio_download = DownloadS3Object(access_key, secret_key, region)
        url = audio_download.generate_download_url(
            bucket_name,
            audio_filepath,
            expiration
        )

        # HttpResponseRedirect to url to download the file.
        # Content Type and Content Disposition force download.
        if url:
            return HttpResponseRedirect(url)
        else:
            messages.error(request, "Sorry, we couldn't download the file.")
            return HttpResponse(status=200)


def get_invitation_id(request, booking_id):
    """
    AJAX Handler to return Invitation ID of a given booking.

    Utilised in dashboard_modals.js file in 'profiles' app.
    To trigger a specific message modal upon page load.
    """
    try:
        requested_booking = Booking.objects.get(pk=booking_id)

        if requested_booking.related_invitation:
            invitation_id = requested_booking.related_invitation.pk
            if invitation_id:
                return JsonResponse({"invitation_id": invitation_id})
    except Booking.DoesNotExist:
        return HttpResponse(status=200)
