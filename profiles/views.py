from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.forms.models import modelformset_factory
from django.conf import settings
from django.contrib.auth.models import User

from bookings.forms import InvitationForm, ReviewForm
from bookings.models import Review

from social.models import Notification
from social.forms import MessageForm
from social.functions import reverse_querystring

from .models import (UserProfile, AudioFile, Equipment,
                     UnavailableDate)
from .forms import UserProfileForm, EquipmentForm, AudioForm
from .functions import (calculate_invite_acceptance_delta,
                        calculate_profile_progress_percentage)

import datetime
import stripe
import logging
import re

# Instantiate Django Logger
logger = logging.getLogger(__name__)


@csrf_exempt
def get_users_unavailable_dates(request, user_id):
    """
    AJAX Handler to retrieve all UnavailableDate objects
    related to a given user.

    Used to populate FullCalendar in EditProfile and Profile views.
    """
    current_user = get_object_or_404(UserProfile, user=user_id)
    unavailable_dates = current_user.unavailable_user.all()
    date_list = []
    for date in unavailable_dates:
        date_list.append(date.date)

    return JsonResponse({"unavailable_dates": date_list})


@csrf_exempt
def get_users_tracks(request, user_id):
    """
    AJAX Handler to retrieve all AudioFile objects
    related to a given user.

    Used to populate music player with user's tracks.
    """
    current_user = get_object_or_404(UserProfile, user=user_id)

    if current_user is not None:
        users_tracks = current_user.users_tracks.all()
        track_list = []
        for track in users_tracks:
            track_object = {
                "name": track.file.name,
                "size": track.file.size
            }
            track_list.append(track_object)

        return JsonResponse({"track_list": track_list})


class ProfileView(TemplateView):
    """
    Profile View
    ------------------

    View to display profile page with user details,
    including:

    - Name
    - Location
    - Instruments Played
    - Audio
    - Unavailable Dates
    - Profile Image
    - Reviews

    Also utilises POST methods to post Invitation
    and Review forms.
    """

    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        username = self.kwargs["user_name"]

        user_profile = get_object_or_404(UserProfile, user__username=username)
        if user_profile.instruments_played:
            instrument_list = user_profile.instruments_played.all()

        if user_profile.users_tracks:
            users_tracks = user_profile.users_tracks.all()

        if user_profile.genres:
            users_genres = user_profile.genres.all()

            track_filename = None
            for track in users_tracks:
                track_file_url = track.file.url
                track_filename = track_file_url.split("/")[-1]

        invitation_form = InvitationForm()

        review_form = ReviewForm(self.request.POST or None)

        # Calculate the average review rating for the user
        users_reviews = user_profile.received_reviews.all()
        num_of_reviews = users_reviews.count()
        average_rating = None

        if user_profile.calculate_average_rating:
            average_rating = (
                user_profile.calculate_average_rating["average_rating"])

        # Insert username of Profile owner into session, to use as
        # reference for Invitation Form.
        self.request.session["invited_username"] = username

        context = {
            "user": user_profile,
            "page_name": "user_profile",
            "instrument_list": instrument_list,
            "users_tracks": users_tracks,
            "users_genres": users_genres,
            "track_filename": track_filename,
            "username": user_profile.user,
            "user_id": user_profile.user.id,
            "invitation_form": invitation_form,
            "review_form": review_form,
            "average_rating": average_rating,
            "num_of_reviews": num_of_reviews
        }

        return context

    def post(self, request, *args, **kwargs):
        """
        Post method to handle data inputted through the Review Form.

        Gets the current context data of profile page and extracts the
        UserProfile value (from "user" key), to add to the new created
        Review instance as the review receiver.

        Review Sender's profile obtained through get_object_or_404,
        and added to Review instance as review sender.

        If form is valid, return to the user's profile with success message.

        If form is invalid, return to the user's profile with error message.
        """

        context = self.get_context_data(**kwargs)

        review_receiver = context["user"]
        review_sender = request.user

        review_receiver_profile = get_object_or_404(
            UserProfile, user__username=review_receiver)

        review_sender_profile = get_object_or_404(
            UserProfile, user__username=review_sender)

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.review_receiver = review_receiver_profile
            form.review_sender = review_sender_profile
            form.save()

            review_receiver_profile.save()
            # Create a notification object to inform review_receiver
            Notification.objects.create(
                notification_sender=review_sender_profile,
                notification_receiver=review_receiver,
                notification_type=6
            )

            # Check if invite receiver profile has a first name.
            # If not, default to the user profile's username.
            # Pass name into success message.
            receiver_name = None
            if review_receiver_profile.first_name:
                receiver_name = review_receiver_profile.first_name
            else:
                receiver_name = review_receiver_profile.user.username
            success_msg = f"You left a review for {receiver_name}"
            return JsonResponse({"success_msg": success_msg})
        else:
            return JsonResponse({"errors": review_form.errors.as_json()})


def get_review_to_edit(request, review_id):
    """
    AJAX GET Handler to retrieve a review object to
    populate the textarea in modal window to edit a given review,
    in the Profile page.

    Upon success, returns a JSON object with review content, otherwise
    a JSON Response is sent, informing the user that the
    Review cannot be found.
    """
    try:
        review = Review.objects.get(pk=review_id)
        review_content = review.review_content
        return JsonResponse({"review": review_content})
    except Review.DoesNotExist:
        return JsonResponse({"error": "Sorry, we can't find the review."})


@require_POST
def edit_review(request, review_id):
    """
    AJAX POST Handler to process data sent through form in the
    Edit Review ModalWindow. Compates the data of field "review_content"
    against regex to check if there are only numbers present in content.
    If so, throw an error.

    If data is valid, update the retrieved review object and save,
    then return a JSON response with success message to display as toast.
    """
    review_to_edit = Review.objects.get(pk=review_id)

    regex = "^[0-9]+$"
    review_content = request.POST.get("review_edit")
    if re.match(regex, review_content):
        return JsonResponse(
            {"error": "Please enter words as well as numbers."})
    else:
        review_to_edit.review_content = request.POST.get("review_edit")
        review_to_edit.rating = request.POST.get("rating")
        review_to_edit.save()
        success_msg = "Your review has been edited."
        return JsonResponse({"success_msg": success_msg})


def edit_profile(request):
    """
    Edit Profile View
    --------------------

    Handles both all GET methods for all form pages of Edit Profile page.

    Retrieves the profile of the user making the request, and displays
    a form for the user to fill in their personal details, as well
    as a list of their equipment and collection of music.

    Utilises the model formset factory to dynamically add extra fields
    to the user's list of equipment.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)

    EquipmentFormsetFactory = modelformset_factory(
        Equipment, form=EquipmentForm, extra=1)

    queryset = user_profile.equipment.all().exclude(equipment_name="")

    equipment_formset = EquipmentFormsetFactory(
        request.POST or None, queryset=queryset)

    audio_form = AudioForm(request.POST, instance=user_profile)

    request.session["form_page"] = 1

    # Provides functionality to switch pages if "Skip Step" button is clicked.
    if request.GET.get("form_page") == str(2):
        request.session["form_page"] = 2
        request.session["page_one_complete"] = False

    # POST request to handle personal details and Equipment Formset
    if request.method == "POST":
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if all([user_profile_form.is_valid(), equipment_formset.is_valid()]):
            parent_form = user_profile_form.save(commit=False)
            parent_form.save()
            user_profile_form.save_m2m()

            for form in equipment_formset:
                child_form = form.save(commit=False)
                if child_form.related_user is None:
                    child_form.related_user = parent_form
                child_form.save()

            messages.success(request, "Profile and Equipment Info Saved.")
            request.session["form_page"] = 2
            request.session["page_one_complete"] = True
    else:
        audio_form = AudioForm(instance=user_profile)
        user_profile_form = UserProfileForm(instance=user_profile or None)

    context = {
        "user_profile_form": user_profile_form,
        "equipment_formset": equipment_formset,
        "audio_form": audio_form,
        "page_name": "user_profile_form",
        "user_id": user_profile.user.id,
    }

    return render(request, "profiles/edit_profile.html", context=context)


def upload_audio(request, username):
    """
    Handles addition or removal of audio files in Edit Profile's
    second page.

    If '{"request": 2}' present in POST request, this informs the view
    that the request is to remove an already-existing audio file from
    the database.

    Otherwise, the audiofile is to be added.
    """

    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":

        # Check whether the request is to upload or remove files.
        # "{'request': 2}" indicates that a file should be removed
        # from database.

        # if not request == 2, upload audio files
        if not request.POST.get("request") == str(2):
            print(request.FILES)
            files = [request.FILES.get('audio[%d]' % i) for i in range(
                     0, len(request.FILES))]
            form = AudioForm(request.POST, instance=user_profile)
            if form.is_valid():
                try:
                    for f in files:
                        AudioFile.objects.create(file=f,
                                                 related_user=user_profile)
                    request.session["form_page"] = 3
                    return HttpResponse(status=200)
                except Exception as e:
                    print("Exception:", e)
            else:
                form = AudioForm(instance=user_profile)

        # Else, find the audiofile to remove, and remove from database
        else:
            audiofile_to_delete = AudioFile.objects.filter(
                file=request.POST.get("filename"), related_user=user_profile
            )
            try:
                logger.info("Trying to delete")
                audiofile_to_delete.delete()
                return HttpResponse(status=200)
            except Exception as e:
                logger.exception("There was an error!")
                print(f"Exception: {e}")
                return HttpResponse(status=500)

    # GET request for AJAX success callback in 'audio_dropzone.js'
    success_msg = "Audio Files Saved"
    return JsonResponse({"form_page": 3, "success_msg": success_msg})


def upload_unavailable_dates(request, user_id):
    """
    AJAX Handler to save unavailable dates to UnavailableDate model.

    Called from calendar.js in Edit Profile page.

    Grabs the date values (as a list) from the data attribute of
    the AJAX post request.

    Loops through the list and creates an UnavailableDate model instance,
    with a ManytoOne relation to the UserProfile instance,
    and saves to the database.

    Upon success, returns as JsonResponse containing a
    success message and the home URL.
    """

    user_profile = get_object_or_404(UserProfile, user=user_id)

    if request.method == "POST":

        # If not request 2, the purpose is to add dates to user's table.
        if not request.POST.get("request") == str(2):
            date_array = request.POST.getlist("date_array[]")
            if date_array is not None:

                # Get user's existing unavailable dates
                users_existing_dates = UnavailableDate.objects.filter(
                    related_user=user_profile)

                # If a date in users_existing_dates matches a date in POST,
                # remove it from POST to avoid duplicates.
                for existing_date in users_existing_dates:
                    for posted_date in date_array:
                        if str(existing_date.date) == posted_date:
                            date_array.remove(posted_date)

                # Create an UnavailableDate object for each date posted
                for date in date_array:
                    try:
                        UnavailableDate.objects.create(
                            date=date, related_user=user_profile)
                    except Exception as e:
                        print(f"Exception: {e}")
                success_msg = "Profile details saved."
                redirect_url = reverse("profile", args=[user_profile.user])
                return JsonResponse({
                    "url": redirect_url, "success_msg": success_msg
                })
        else:
            # If request 2, the purpose is to remove dates from user's table.
            existing_unavailable_dates = user_profile.unavailable_user.all()
            date_to_remove = request.POST.get("event_to_remove")
            date_to_remove = datetime.datetime.strptime(
                date_to_remove, "%Y-%m-%d").date()

            for unavailable_date in existing_unavailable_dates:
                if unavailable_date.date == date_to_remove:
                    date_object_to_remove = UnavailableDate.objects.filter(
                        date=date_to_remove, related_user=user_profile)
                    date_object_to_remove.delete()

            return HttpResponse(status=200)


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard View
    -----------------------

    Displays a complete collection of a given user's metrics,
    active/inactive jobs, and a link to manage their subscription.

    Metrics include:

    - Profile Completedness
    - Review Rating
    - Invitation Acceptance Delta
    - Subscription Status

    Job Page Includes:

    - All Tier One engagements with sections 'Invitations Sent'
      and 'Inivatations Received'. Filterable by All, Pending and Confirmed.

    - (If paid), All Tier Two engagements with sections 'Offers Sent'
      and 'My Posted Jobs'. Filterable by All, Pending and Confirmed.

    A link in the page's navbar is also displayed, to allow the user
    to manage their subscription.
    """

    template_name = "profiles/dashboard.html"

    def get(self, *args, **kwargs):
        """
        Restricts access to users visiting another user's Dashboard.
        Checks endpoint slug against request user's slug, and redirects
        away from Dashboard page if they do not match.
        """

        current_user = get_object_or_404(
            UserProfile, user__username=self.request.user)

        url_path = self.request.get_full_path()

        # Restrict access to Dashboard page to request user who
        # owns the profile object.
        user_check = "".join(url_path.split("/")[3])
        if "?" in url_path:
            user_check = user_check.split("?")[0]
        if not current_user.slug == user_check:
            messages.warning(
                self.request,
                mark_safe("You may not visit another member's dashboard."))
            return redirect(reverse_querystring("dashboard",
                                                args=[current_user.slug],
                                                query_kwargs={
                                                    "page": "jobs",
                                                    "section": "tier_one"
                                                }))

        # Restrict access to Tier Two content if user profile doesn't
        # have "is_paid" status.
        tier_check = None
        if "&" in url_path:
            tier_check = "".join(url_path.split("&")[1])
            if tier_check == "section=tier_two":
                if not current_user.is_paid:
                    messages.warning(
                        self.request,
                        mark_safe("You do not have Tier Two access."))
                    return redirect(
                        reverse_querystring("dashboard",
                                            args=[current_user.slug],
                                            query_kwargs={
                                                "page": "jobs",
                                                "section": "tier_one"
                                            }))
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Override default get_context_data to get user's dashboard data:

        - Invites they need to respond to
        - Completeness of their profile
        - Invitations sent and received

        """
        context = super().get_context_data(**kwargs)
        current_user = self.kwargs["slug"]

        user_profile = get_object_or_404(UserProfile, slug=current_user)
        username = user_profile.user.username

        # Calculate number of invites the user has to respond to
        invite_acceptance_delta = (
            calculate_invite_acceptance_delta(username))

        profile_progress_percentage = (
            calculate_profile_progress_percentage(username))

        received_reviews = user_profile.received_reviews.all()
        num_of_reviews = user_profile.received_reviews.count()
        average_rating = 0
        if received_reviews:
            average_rating = (
                user_profile.calculate_average_rating["average_rating"])

        current_page = "dashboard"
        current_section = "tier_one"
        current_subsection = "invites_received"
        current_filter = "all"

        # Grab Booking ID if user is visiting dashboard from
        # booking details page (clicking 'Message User')

        referer_url_path = None
        referer_url = self.request.META.get("HTTP_REFERER")

        # Get the referal url path (looking for "bookings" or
        # "bookings/edit_invitation")
        if referer_url is not None:
            referer_url_path = "/".join(referer_url.split("/")[3:-1])

        booking_id = None
        invitation_id = None

        # Set filter to Booking ID if user visiting dashboard
        # from Booking Success/Detail Page.
        if (referer_url_path == "bookings/success"
            or referer_url_path == "bookings/booking_detail"):
            booking_id = self.request.GET.get("filter")

        # # Set filter to Invitation ID if user visiting dashboard
        # # from Edit Invitation Page.
        elif referer_url_path == "bookings/edit_invitation":
            invitation_id = self.request.GET.get("filter")

        job_id = self.request.GET.get("filter")

        # Set filter to Invitation ID if user visiting dashboard
        # by clicking notification "<user> has invited you to play <event>"
        if "invitation_id" in self.request.session:
            invitation_id = self.request.GET.get("filter")

        invitations_sent = None
        invitations_received = None
        posted_jobs = None
        offers_sent = None

        """
        Change pages and nested sections of dashboard page.
        Filter invitations relative to URL filter params:
        All - Pending - Accepted - Completed
        """
        if "page" in self.request.GET:
            current_page = self.request.GET["page"]
            if "section" in self.request.GET:
                current_section = self.request.GET["section"]
                if current_section == "tier_one":
                    if "subsection" in self.request.GET:
                        current_subsection = self.request.GET["subsection"]
                        if current_subsection == "invites_sent":
                            if "filter" in self.request.GET:
                                current_filter = self.request.GET["filter"]
                                if current_filter == "all":
                                    invitations_sent = (
                                        user_profile.invitations_sent
                                        .all())
                                elif current_filter == "pending":
                                    invitations_sent = (
                                        user_profile.invitations_sent
                                        .filter(
                                            is_accepted=False))
                                elif current_filter == "accepted":
                                    invitations_sent = (
                                        user_profile.invitations_sent
                                        .filter(
                                            is_accepted=True))
                                elif current_filter == booking_id:
                                    invitations_sent = (
                                        user_profile.invitations_sent
                                        .filter(related_booking__pk=booking_id)
                                        )
                                elif current_filter == invitation_id:
                                    invitations_sent = (
                                        user_profile.invitations_sent
                                        .filter(pk=invitation_id))
                        elif current_subsection == "invites_received":
                            if "filter" in self.request.GET:
                                current_filter = self.request.GET["filter"]
                                if current_filter == "all":
                                    invitations_received = (
                                        user_profile.invitations_received
                                        .all())
                                elif current_filter == "pending":
                                    invitations_received = (
                                        user_profile.invitations_received
                                        .filter(is_accepted=False)
                                        )
                                elif current_filter == "accepted":
                                    invitations_received = (
                                        user_profile.invitations_received
                                        .filter(is_accepted=True))
                                elif current_filter == booking_id:
                                    invitations_received = (
                                        user_profile.invitations_received
                                        .filter(related_booking__pk=booking_id)
                                        )
                                elif current_filter == invitation_id:
                                    invitations_received = (
                                        user_profile.invitations_received
                                        .filter(pk=invitation_id)
                                        )
                elif current_section == "tier_two":
                    if "subsection" in self.request.GET:
                        current_subsection = self.request.GET["subsection"]
                        if current_subsection == "posted_jobs":
                            if "filter" in self.request.GET:
                                current_filter = self.request.GET["filter"]
                                if current_filter == "all":
                                    posted_jobs = (
                                        user_profile.posted_jobs.all())
                                elif current_filter == "pending_offers":
                                    posted_jobs = (
                                        user_profile.posted_jobs
                                        .filter(is_taken=False,
                                                interested_member__gt=0))
                                elif current_filter == "confirmed":
                                    posted_jobs = (
                                        user_profile.posted_jobs
                                        .filter(is_taken=True)
                                        )
                                elif current_filter == job_id:
                                    posted_jobs = (
                                        user_profile.posted_jobs
                                        .filter(pk=job_id)
                                        )
                        elif current_subsection == "offers_sent":
                            if "filter" in self.request.GET:
                                current_filter = self.request.GET["filter"]
                                if current_filter == "all":
                                    offers_sent = user_profile.job_set.all()
                                elif current_filter == "pending_offers":
                                    offers_sent = (
                                        user_profile.job_set
                                        .all()
                                        .exclude(is_taken=True))
                                elif current_filter == "confirmed":
                                    offers_sent = (
                                        user_profile.job_set.filter(
                                            confirmed_member=user_profile))
                                elif current_filter == job_id:
                                    offers_sent = (
                                        user_profile.job_set
                                        .filter(pk=job_id)
                                        )

        # Stripe Price ID to inject into hidden input
        tier_two_price_id = settings.STRIPE_TIERTWO_PRICE_ID

        # Render text input in "Message <user>" modal
        message_form = MessageForm()

        context = {
            "user_profile": user_profile,
            "invite_acceptance_delta": invite_acceptance_delta,
            "profile_progress_percentage": profile_progress_percentage,
            "page_name": "dashboard",
            "current_user": current_user,
            "current_page": current_page,
            "current_section": current_section,
            "current_subsection": current_subsection,
            "current_filter": current_filter,
            "tier_two_price_id": tier_two_price_id,
            "invitations_sent": invitations_sent,
            "invitations_received": invitations_received,
            "received_reviews": received_reviews,
            "average_rating": average_rating,
            "num_of_reviews": num_of_reviews,
            "message_form": message_form,
            "posted_jobs": posted_jobs,
            "offers_sent": offers_sent
        }

        return context


def delete_account(request, profile_id):
    """
    Deletes a given User object, identified through
    the associated UserProfile object's ID.
    """
    current_user_profile = get_object_or_404(UserProfile, pk=profile_id)
    auth_user = User.objects.get(username=current_user_profile.user.username)

    # Ensure that a user can't maliciously delete another user's profile
    # by typing in the URL manually.
    if auth_user != request.user:
        messages.warning(
            request, mark_safe("You can't delete another member's profile!"))
        return redirect(reverse("home"))
    try:
        delete_stripe_customer(auth_user.email)
        auth_user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect(reverse("home"))
    except User.DoesNotExist:
        messages.error(request, "This user doesn't exist.")
        return redirect(reverse("profile", args=[auth_user.username]))
    except Exception as e:
        messages.error(request, f"Sorry, there was an error: {e}")
        return redirect(reverse("profile", args=[auth_user.username]))


def delete_stripe_customer(customer_email):
    """
    Retrieves the user's stripe account details from the Stripe API
    and deletes them from the stripe database, cancelling their
    subscription automatically.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    get_stripe_customer = stripe.Customer.list(email=customer_email)
    if get_stripe_customer:
        stripe_customer_id = get_stripe_customer.data[0].id
        try:
            stripe.Customer.delete(stripe_customer_id)
            return HttpResponse(status=200)
        except Exception:
            return HttpResponse(status=404)
    else:
        return None
