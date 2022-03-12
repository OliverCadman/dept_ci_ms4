from ast import parse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.contrib import messages

from dateutil import parser

from .forms import JobForm
from profiles.models import UserProfile, Instrument, Genre

from .functions import handle_deplist_get




class DepListView(ListView):
    """
    A view to display all individual UserProfile objects.

    In addition to displaying all UserProfile objects,
    DepListView also takes parameters for searching.
    
    """

    template_name = "jobs/dep_list.html"

    model = UserProfile

    context_object_name = "dep_collection"


    paginate_by = 8

    def get_queryset(self):
        """
        Override default get_queryset method to handle
        extra filter params.
        """

        # Get the current context with any params included.
        self.pre_context = handle_deplist_get(self.request.GET)

        # Filter the UserProfile table with provided search params.
        query = UserProfile.objects.filter_queryset(
            filter_params=self.pre_context["search_params"],
            date_today=self.pre_context["available_today"]
        )

        return query

    def get_context_data(self, **kwargs):
        """
        Override default get_context_data to provided additional
        pre-prepared context, prepared in View's "get_queryset" method.
        """
        context =  super().get_context_data(**kwargs) | self.pre_context
        
        if self.get_queryset == None:
            context["no_results"] = True

        # Page name required in order to render correct header content.
        context["page_name"] = "dep_list"

        # Query for a complete list of instruments, used to filter results 
        # by instrument.
        instrument_list = Instrument.objects.all()
        context["instrument_list"] = instrument_list

        # Query for a complete list of genres, used to filter requlest
        # by genre.
        genre_list = Genre.objects.all()
        context["genre_list"] = genre_list

        # Populates the "selected_city" context key with a value.
        # Used to populate the search bar with city searched by user
        # upon page refresh.
        context["selected_city"] = context["city"]

        # Populates the "availabletoday_checkbox_selected" context key with a value.
        # Used to check the related checkbox upon page refresh (if checked by the user).
        context["availabletoday_checkbox_selected"] = context["available_today"] 

        # Used to apply the 'selected' attribute to the selected 
        # filter criteria in "Instrument" form select.
        context["selected_instrument"] = context["instrument"]

        context["selected_genre"] = context["genre"]

        return context


class JobView(TemplateView):
    """
    A view to display all Job Posts, and handle
    POST request send from JobForm.
    """
    template_name = "jobs/job_list.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        job_form = JobForm()

        context = {
            "page_name": "job_list",
            "job_form": job_form
        }

        return context

    
    def post(self, request):
        """
        Handles Job Form submission from "Find a Job" Page.
        """
        
        # Grab request user's profile to include in Job instance creationg
        # as "job_poster".
        current_user = request.user
        user_profile = get_object_or_404(UserProfile, user__username=current_user)
    

        # Parse the datetime field into python datetime object,
        # readable by Django.
        event_datetime = request.POST.get("event_datetime")
        parsed_datetime = parser.parse(event_datetime)

        # Prepare new request dictionary to allow inclusion of 
        # prepared datetime field.
        job_post_request = {
            "job_title": request.POST.get("job_title"),
            "event_name": request.POST.get("event_name"),
            "artist_name": request.POST.get("artist_name"),
            "job_description": request.POST.get("job_description"),
            "fee": request.POST.get("fee"),
            "event_city": request.POST.get("event_city"), 
            "event_country": request.POST.get("event_country"),
            "event_datetime": parsed_datetime,
        }

        # Create JobForm object with post request included
        job_form = JobForm(job_post_request)

        if job_form.is_valid():
            form = job_form.save(commit=False)
            form.job_poster = user_profile
            form.save()
            messages.success(request, "Your job has been posted.")
            return redirect(reverse("job_list"))
        else:
            print(job_form.errors)
            messages.error(request, "Please make sure your form is valid.")
            return redirect(reverse("job_list"))


