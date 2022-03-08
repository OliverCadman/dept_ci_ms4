from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from profiles.models import UserProfile


class JobPageView(View):

    def get(self, request, job_name):
        print(job_name)
        return render(request, "jobs/job_list.html")

class FindADepLandingPageView(ListView):

    template_name = "jobs/dep_list.html"

    model = UserProfile

    context_object_name = "dep_collection"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["page_name"] = "dep_list"
        return context




