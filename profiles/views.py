from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.forms.models import modelformset_factory
from django.conf import settings

from bookings.models import Invitation
from bookings.forms import InvitationForm, ReviewForm
from .models import UserProfile, AudioFile, Equipment, UnavailableDate

from social.forms import MessageForm
from .forms import UserProfileForm, EquipmentForm, AudioForm

from .functions import calculate_invite_acceptance_delta, calculate_profile_progress_percentage


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

        review_form = ReviewForm()

        
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
            "review_form": review_form
        }

        return context


def edit_profile(request):

    print("EDIT PROFILE REQUEST")
    print(request)

    user_profile = get_object_or_404(UserProfile, user=request.user)
    EquipmentFormsetFactory = modelformset_factory(Equipment, form=EquipmentForm, extra=1)
    queryset = user_profile.equipment.all()
    equipment_formset = EquipmentFormsetFactory(request.POST or None, queryset=queryset)
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
    
    success_msg = "Audio Files Saved"
    
    return JsonResponse({"form_page": 3, "success_msg": success_msg})



def upload_unavailable_dates(request, user_id):

    user_profile = get_object_or_404(UserProfile, user=user_id)

    if request.method == "POST":
        date_array = request.POST.getlist("date_array[]")
        if date_array is not None:
            for date in date_array:
                try:
                    UnavailableDate.objects.create(date=date, related_user=user_profile)
                    success_msg = "Congratulations, your profile is complete!"
                    return JsonResponse({"url": "/", "success_msg": success_msg})
                except Exception as e:
                    messages.error("Sorry, something went wrong.")
                    return HttpResponse(status=500)

            messages.success(request, "Unavailable Dates saved")

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
            "message_form": message_form
        }

        return context
