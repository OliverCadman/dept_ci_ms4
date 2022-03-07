from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class JobPageView(View):

    def get(self, request, job_name):
        print(job_name)
        return render(request, "jobs/job_list.html")

class FindADepLandingPageView(View):

    def get(self, request, *args, **kwargs):

        context = {
        "page_name": "find_a_dep_landing_page"
        }
    
        return render(request, "jobs/findadep_landing_page.html", context=context)



