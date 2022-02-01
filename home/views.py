from django.shortcuts import render, redirect
from django.views import View

from django.conf import settings


class IndexView(View):
    def get(self, request):
        
        referrer_url = request.META.get("HTTP_REFERER")
        if referrer_url is not None:
            
            if referrer_url == f"{settings.DOMAIN_NAME}accounts/signup/":
                return redirect("profile", request.user)
            else:
                print(False)

            

        return render(request, "home/index.html")