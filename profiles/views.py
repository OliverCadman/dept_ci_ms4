from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import View

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.forms.models import modelformset_factory

from .models import UserProfile, AudioFile, Equipment, UnavailableDate
from .forms import UserProfileForm, EquipmentForm, AudioForm


@csrf_exempt
def get_users_unavailable_dates(request, username):
    current_user = get_object_or_404(UserProfile, user=username)
    print(username)
    # TODO: Change related name of object

    unavailable_dates = current_user.unavailable_user.all()
    date_list = []
    for date in unavailable_dates:
        date_list.append(date.date)

    return JsonResponse({"unavailable_dates": date_list})


@csrf_exempt
def get_users_tracks(request, username):
    current_user = get_object_or_404(UserProfile, user=username)

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



class ProfileView(View):

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.instruments_played:
            instrument_list = user_profile.instruments_played.all()

        if user_profile.users_tracks:
            users_tracks = user_profile.users_tracks.all()

        if user_profile.genres:
            users_genres = user_profile.genres.all()
            

            for track in users_tracks:
                track_file_url = track.file.url
                track_filename = track_file_url.split("/")[-1]

        context = {
            "user": user_profile,
            "page_name": "user_profile",
            "instrument_list": instrument_list,
            "users_tracks": users_tracks,
            "users_genres": users_genres,
            "track_filename": track_filename,
            "username": user_profile.user.id
         
        }
        return render(request, "profiles/profile.html", context=context)


def edit_profile(request, username):

    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_profile_form = UserProfileForm(request.POST, instance=user_profile)
    EquipmentFormsetFactory = modelformset_factory(Equipment, form=EquipmentForm, extra=0)
    queryset = user_profile.equipment.all()
    equipment_formset = EquipmentFormsetFactory(request.POST or None, queryset=queryset)

    audio_form = AudioForm(request.POST, instance=user_profile)

    print(user_profile.users_tracks.all())

    request.session["form_page"] = 1

    if request.method == "POST":
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
            print(user_profile_form.errors)   
    else:
        audio_form = AudioForm(instance=user_profile)
        print(audio_form)
        user_profile_form = UserProfileForm(instance=user_profile or None)

    context = {
        "user_profile_form": user_profile_form,
        "equipment_formset": equipment_formset,
        "audio_form": audio_form,
        "page_name": "user_profile_form",
        "user_name": user_profile.user.id,
    }

    return render(request, "profiles/edit_profile.html", context=context)


def upload_audio(request, username):

    user_model = get_user_model()
    current_user = user_model.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=current_user)

    print(user_profile.city)


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
            form = AudioForm(instance=current_user)
    
    success_msg = "Audio Files Saved"
    
    return JsonResponse({"form_page": 3, "success_msg": success_msg})


def upload_unavailable_dates(request, username):

    user_profile = get_object_or_404(UserProfile, user=request.user)

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


