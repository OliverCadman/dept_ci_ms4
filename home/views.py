from django.shortcuts import render, redirect
from django.views import View

from django.contrib import messages
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile


class IndexView(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            current_user = get_object_or_404(UserProfile, user__username=request.user)

            if not current_user.subscription_chosen:
                messages
                return redirect("subscribe/choose_subscription")

        return render(request, "home/index.html")