from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.forms.models import modelformset_factory
from django.conf import settings

from bookings.models import Invitation, Review
from bookings.forms import InvitationForm, ReviewForm
from .models import UserProfile, AudioFile, Equipment, UnavailableDate

from social.forms import MessageForm
from .forms import UserProfileForm, EquipmentForm, AudioForm

from .functions import calculate_invite_acceptance_delta, calculate_profile_progress_percentage

import datetime


@csrf_exempt
def get_users_unavailable_dates(request, username):
    current_user = get_object_or_404(UserProfile, user=username)
    # TODO: Change related name of object

    unavailable_dates = current_user.unavailable_user.all()
    date_list = []
    for date in unavailable_dates:
        date_list.append(date.date)

    return JsonResponse({"unavailable_dates": date_list})


@csrf_exempt
def get_users_tracks(request, user_id):
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
            average_rating = user_profile.calculate_average_rating["average_rating"]
        
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

        print(context["review_form"].fields["review_content"])

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

        review_receiver_profile = context["user"]
        review_sender = request.user


        review_sender_profile = get_object_or_404(UserProfile, user__username=review_sender)

        
        review_form = context["review_form"]
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.review_receiver = review_receiver_profile
            form.review_sender = review_sender_profile
            form.save()

            # Check if invite receiver profile has a first name.
            # If not, default to the user profile's username.
            # Pass name into success message.
            receiver_name = None
            if review_receiver_profile.first_name:
                receiver_name = review_receiver_profile.first_name
            else:
                receiver_name = review_receiver_profile.user.username
            messages.success(request, f"You left a review for {receiver_name}")
            return redirect(reverse("profile", args=[review_receiver_profile.user.username]))
        else:
            context = self.get_context_data(**kwargs)
            context["review_form"] = ReviewForm()

            messages.error(request, "Review failed to send. Please make sure your review is valid.")
            return redirect(reverse("profile", args=[review_receiver_profile.user.username]), context=context)



def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    EquipmentFormsetFactory = modelformset_factory(Equipment, form=EquipmentForm, extra=1)
    queryset = user_profile.equipment.all().exclude(equipment_name="")
    equipment_formset = EquipmentFormsetFactory(request.POST or None, queryset=queryset)
    print(equipment_formset)
    audio_form = AudioForm(request.POST, instance=user_profile)

    request.session["form_page"] = 1

    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if all([user_profile_form.is_valid(), equipment_formset.is_valid()]):
            try:
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
                        
            except Exception as e:
                print(f"Exception: {e}")
        else:
            print("form invalid")
            print(user_profile_form.errors)   
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

    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":

        # Check whether the request is to upload or remove files.
        # "{'request': 2}" indicates that a file should be removed from database.

        # if not request == 2, upload audio files
        if not request.POST.get("request") == str(2):
            files = [request.FILES.get('audio[%d]' % i) for i in range(0, len(request.FILES))] 
            form = AudioForm(request.POST, instance=user_profile)
            if form.is_valid():
                try:
                    for f in files:
                        AudioFile.objects.create(file=f, related_user=user_profile)
                    request.session["form_page"] = 3
                    return HttpResponse(status=200)
                except Exception as e:
                    print("Exception:", e)
            else:
                print("form invalid")
                form = AudioForm(instance=user_profile)

        # Else, remove audio file from database        
        else:
            audiofile_to_delete =  get_object_or_404(AudioFile, file=request.POST.get("filename"))
            try:
                audiofile_to_delete.delete()
                messages.success(request, "Audio file removed")
                return HttpResponse(status=200)
            except Exception as e:
                print(f"Exception: {e}")
                messages.error(request, "Sorry, there was an error.")
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
    with a ManytoOne relation to the UserProfile instance, and saves to the database.

    Upon success, returns as JsonResponse containing a success message and the home URL.
    """

    user_profile = get_object_or_404(UserProfile, user=user_id)

    if request.method == "POST":
        if not request.POST.get("request") == str(2):
            date_array = request.POST.getlist("date_array[]")
            if date_array is not None:
                print("date array")
                print(date_array)
                for date in date_array:
                    try:
                        UnavailableDate.objects.create(date=date, related_user=user_profile)
                    except Exception as e:
                        print(f"Exception: {e}")
            success_msg = "Profile details saved."
            return JsonResponse({ "url": "/", "success_msg": success_msg})
        else:
            existing_unavailable_dates = user_profile.unavailable_user.all()
            date_to_remove = request.POST.get("event_to_remove")
            date_to_remove = datetime.datetime.strptime(date_to_remove, "%Y-%m-%d").date()
            for unavailable_date in existing_unavailable_dates:
                if unavailable_date.date == date_to_remove:
                    date_object_to_remove = UnavailableDate.objects.filter(date=date_to_remove, related_user=user_profile)
                    date_object_to_remove.delete()
            return HttpResponse(status=200)


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "profiles/dashboard.html"

    def get(self, *args, **kwargs):
        """
        Disables a user from visiting another user's Dashboard.
        Checks endpoint slug against request user's slug, and redirects
        away from Dashboard page if they do not match.
        """

        current_user = get_object_or_404(UserProfile, user__username=self.request.user)

        url_path = self.request.get_full_path()
        url_endpoint = "".join(url_path.split("/")[3])
        if "?" in url_endpoint:
            url_endpoint = "".join(url_endpoint.split("?")[0])
         
        if not current_user.slug == url_endpoint:
            messages.info(self.request, mark_safe("You may not visit another member's dashboard."))
            return redirect(reverse("home"))
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
        invite_acceptance_delta = calculate_invite_acceptance_delta(username)
        profile_progress_percentage = calculate_profile_progress_percentage(username)

        received_reviews = user_profile.received_reviews.all()
        print(received_reviews)
        average_rating = 0
        if received_reviews:
            average_rating = user_profile.calculate_average_rating
            print(average_rating)

        current_page = "dashboard"
        current_section = "invites_sent"
        current_filter = "all"

        # Grab Booking ID if user is visiting dashboard from
        # booking details page (clicking 'Message User')

        referer_url = self.request.META.get("HTTP_REFERER")
        referer_url_path = referer_url.split("/")[3]

        # Set filter to Booking ID if user visiting dashboard
        # from Booking Detail Page.
        booking_id = None
        if referer_url_path == "bookings":
            booking_id = self.request.GET.get("filter")
        
        # Set filter to Invitation ID if user visiting dashboard
        # by clicking notification "<user> has invited you to play <event>"
        invitation_id = None
        if "invitation_id" in self.request.session:
            invitation_id = self.request.GET.get("filter")

        invitations_sent = None
        invitations_received = None

        """
        Change pages and nested sections of dashboard page.
        Filter invitations relative to URL filter params:
        All - Pending - Accepted - Completed
        """
        if "page" in self.request.GET:
            current_page = self.request.GET["page"]
            if "section" in self.request.GET:
                current_section = self.request.GET["section"]
                if current_section == "invites_sent":
                    if "filter" in self.request.GET: 
                        current_filter = self.request.GET["filter"]
                        if current_filter == "all":
                            invitations_sent = user_profile.invitations_sent.all()
                        elif current_filter == "pending":
                            invitations_sent = user_profile.invitations_sent.filter(is_accepted=False)
                        elif current_filter == "accepted":
                            invitations_sent = user_profile.invitations_sent.filter(is_accepted=True)
                elif current_section == "invites_received":
                    if "filter" in self.request.GET:
                        current_filter = self.request.GET["filter"]
                        if current_filter == "all":
                            invitations_received = user_profile.invitations_received.all()
                        elif current_filter == "pending":
                            invitations_received = user_profile.invitations_received.filter(is_accepted=False)
                        elif current_filter == "accepted":
                            invitations_received = user_profile.invitations_received.filter(is_accepted=True)
                        elif current_filter == booking_id:
                            invitations_received = user_profile.invitations_received.filter(
                                related_booking__pk=booking_id)
                        elif current_filter == invitation_id:
                            invitations_received = user_profile.invitations_received.filter(
                                pk=invitation_id
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
            "current_page" : current_page,
            "current_section": current_section,
            "tier_two_price_id": tier_two_price_id,
            "invitations_sent": invitations_sent,
            "invitations_received": invitations_received,
            "received_reviews": received_reviews,
            "average_rating": average_rating,
            "message_form": message_form,

        }

        return context
