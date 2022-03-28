from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from django.shortcuts import get_object_or_404

from profiles.models import UserProfile


class IndexView(View):
    """
    Index View
    ------------------

    Displays the website's home page.
    """
    def get(self, request):
        """
        GET request to display the website's
        home page.
        """
        return render(request, "home/index.html")
