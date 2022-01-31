from django.shortcuts import render
from django.views import View


class JobPageView(View):

    def get(self, request, job_name):
        print(job_name)
        return render(request, "jobs/job_list.html")



