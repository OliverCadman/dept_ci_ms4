from django.shortcuts import render
from django.views import View
from django.http import HttpRequest



class ProfileView(View):
    
    def get(self, request, user_name):
        print("Request:", request.META.get("HTTP_REFERER"))
        return render(request, "profiles/profile.html")
