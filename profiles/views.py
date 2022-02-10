from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.forms.models import modelformset_factory

from .models import UserProfile, AudioFile, Equipment
from .forms import UserProfileForm, EquipmentForm, AudioForm
from .validators import validate_audiofile
from .functions import get_user_profile, prepare_form_data



class ProfileView(View):
    
    def get(self, request, user_name):
        print("Request:", request.META.get("HTTP_REFERER"))
        return render(request, "profiles/profile.html")


def edit_profile(request, username):

    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_profile_form = UserProfileForm(request.POST, instance=user_profile)
    EquipmentFormsetFactory = modelformset_factory(Equipment, form=EquipmentForm, extra=0)
    queryset = user_profile.equipment.all()
    equipment_formset = EquipmentFormsetFactory(request.POST or None, queryset=queryset)

    audio_form = AudioForm(request.POST, instance=user_profile)

    request.session["form_page"] = 1

    if request.method == "POST":
        print("Request")
        print(request.POST)
        if all([user_profile_form.is_valid(), equipment_formset.is_valid()]):
            try:
                parent_form = user_profile_form.save(commit=False)
                parent_form.save()
                for form in equipment_formset:
                    child_form = form.save(commit=False)
                    if child_form.related_user is None:
                        print("Added new")
                        child_form.related_user = parent_form
                    child_form.save()

                messages.success(request, "Profile and Equipment Info Saved.")
                request.session["form_page"] = 2
                        
            except Exception as e:
                print(f"Exception: {e}")
        else:
            print(user_profile_form.errors)   
    else:
        audio_form = AudioForm()
        user_profile_form = UserProfileForm()

    context = {
        "user_profile_form": user_profile_form,
        "equipment_formset": equipment_formset,
        "audio_form": audio_form,
        "page_name": "user_profile_form",
        "user_name": user_profile.user,
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

                messages.success(request, "Audio Files Saved")
                request.session["form_page"] = 3
                return HttpResponse(status=200)
            except Exception as e:
                print("Exception:", e)
        else:
            print("form invalid")
            form = AudioForm(instance=current_user)
    
    success_msg = "Audio Files Saved"
    
    return JsonResponse({"form_page": 3, "success_msg": success_msg})


