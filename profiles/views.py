import re

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

    user_model = get_user_model()
    current_user = user_model.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=current_user)

    queryset = Equipment.objects.all()
    print(queryset)    

    user_profile_form = UserProfileForm(request.POST, instance=user_profile)

    EquipmentFormset = modelformset_factory(Equipment, form=EquipmentForm, extra=5)
    equipment_formset = EquipmentFormset(request.POST or None, queryset=queryset)

    
    if request.POST.get("action") == "post":
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
        "user_name": current_user.username
    }

    return render(request, "profiles/edit_profile.html", context=context)


def upload_audio(request, username):

    user_model = get_user_model()
    current_user = user_model.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=current_user)

    print(user_profile.city)


    if request.method == "POST":
        
        data_to_dict = dict(request.FILES)
        
        for key, value in data_to_dict.items():

            audio_file = value
            print("audio_file:", audio_file)
            audio_dict = prepare_form_data(
                key="file", value=audio_file
            )

            print("audio_dict", audio_dict)
            form = AudioForm(audio_dict, instance=user_profile)
            print(form.instance)
            if form.is_valid():
                try:
                    # validated_form = form.save(commit=False)
                    # validated_form.related_user = user_profile
                    form.save()
                    print("success")
                except Exception as e:
                    print("Exception:", e)
                return HttpResponse(status=200)
            else:
                print("form invalid")
                form = AudioForm(audio_dict, instance=current_user)
    
    return HttpResponse(status=200)


