from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages

from .forms import InvitationForm

# Create your views here.

def invitation_form_view(request):
    if request.POST:
        
        messages.success(request, "Invitation Sent")
        return redirect(reverse("profile", kwargs={"user_name": request.user}))
    