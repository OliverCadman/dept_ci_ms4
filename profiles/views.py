import re

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model

from .models import UserProfile

from .forms import UserProfileForm, EquipmentForm



class ProfileView(View):
    
    def get(self, request, user_name):
        print("Request:", request.META.get("HTTP_REFERER"))
        return render(request, "profiles/profile.html")
        

def edit_profile(request, username):

    user_model = get_user_model()

    current_user = user_model.objects.get(username=username)
    print(current_user.id)
    user_profile = UserProfile.objects.get(user=current_user)


    if request.method == "POST":
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)

            if user_profile_form.is_valid():
                try:
                    user_profile_form.save()
                except Exception as e:
                    print(f"Exception: {e}")
            else:
                print(user_profile_form.errors)

            equipment_data = request.POST.getlist("equipment_name")

            equipment_dict = None
            for value in equipment_data:
                equipment_dict = {
                    "equipment_name": value
                }

                equipment_form=EquipmentForm(equipment_dict)

                if equipment_form.is_valid():
                    try:
                        post = equipment_form.save(commit=False)
                        post.related_user = user_profile
                        post.save()
                    except Exception as e:
                        print(f"Exception with Equipment Form: {e}")

            equipment_form = EquipmentForm(request.POST, instance=user_profile)

        
    else:
        user_profile_form = UserProfileForm()
        equipment_form = EquipmentForm()
  

    context = {
        "user_profile_form": user_profile_form,
        "equipment_form": equipment_form,
        "page_name": "user_profile_form",
        "user_name": current_user.username
    }

    return render(request, "profiles/edit_profile.html", context=context)


