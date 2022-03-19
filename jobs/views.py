from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, UpdateView
from django.contrib import messages
from django.utils.safestring import mark_safe

from dateutil import parser

from .forms import JobForm
from .models import Job

from profiles.models import UserProfile, Instrument, Genre, AudioFile
from bookings.models import Booking

from .functions import handle_get_params

from pathlib import Path


class DepListView(ListView):
    """
    A view to display all individual UserProfile objects.

    In addition to displaying all UserProfile objects,
    DepListView also takes parameters for searching and/or filtering.
    """

    template_name = "jobs/dep_list.html"

    model = UserProfile
    print(model)
    context_object_name = "dep_collection"

    paginate_by = 8

    def get_queryset(self):
        """
        Override default get_queryset method to handle
        extra filter params.
        """

        # Get the current context with any params included.
        self.pre_context = handle_get_params(self.request.GET)

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

        # Merge base context with pre context from "handle_get_params()"
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


class JobListView(ListView):
    """
    A view to display all Job Posts.

    In addition to displaying all Job objects,
    DepListView also takes parameters for searching and/or filtering.
    """

    template_name = "jobs/job_list.html"
    model = Job
    context_object_name = "job_collection"
    paginate_by = 6

    def get_context_data(self, **kwargs):

        # Merge base context with pre context from "handle_get_params()"
        context =  super().get_context_data(**kwargs) | self.pre_context

        job_form = JobForm()

        # Pass page name to header "includes"
        context["page_name"] = "job_list"

        # Pass job form to page
        context["job_form"] = job_form

        # Populates the "selected_fee" context key with min and max value,
        # and sets relative option attribute to selected if the value matches.
        context["selected_fee"] = f"{context['min_fee']}-{context['max_fee']}"
 
        # Populate the "instrument" select dropdown with values from Instrument Model.
        context["instrument_list"] = Instrument.objects.all()

        if self.request.user.is_authenticated:

            current_user = get_object_or_404(UserProfile, user__username=self.request.user.username)

            # Get current user's jobs to personalize CTA buttons (if they have expressed interest)
            current_users_jobs = current_user.job_set.all()

            context["current_user"] = current_user
            context["current_users_jobs"] = current_users_jobs

        return context

    
    def get_queryset(self):

        """
        Override default get_queryset method to handle
        extra filter params, including min and max fee.
        """

        self.pre_context = handle_get_params(self.request.GET)

        query = Job.objects.filter_queryset(
            filter_params=self.pre_context["search_params"],
            min_fee=self.pre_context["min_fee"],
            max_fee=self.pre_context["max_fee"]
        )
        return query


def post_job(request):
    """
    Handles Job Form submission from "Find a Job" Page.
    """

    # Grab request user's profile to include in Job instance creationg
    # as "job_poster".
    current_user = request.user
    user_profile = get_object_or_404(UserProfile, user__username=current_user)

    # Restrict access to post_job view if current user does not have "is_paid" status.
    if not user_profile.is_paid:
        messages.warning(request, "You need to be a Tier Two member to post a job.")
        return redirect(reverse("job_list"))

    if request.method == "POST":
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
        job_form = JobForm(job_post_request, request.FILES)

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

        

class EditJobView(UpdateView):

    """
    Updates a given Job object using JobForm,
    with fields pre-populated with values inputted by the 
    invite sender from submitting the original form from
    the job list page.
    """

    template_name = "jobs/edit_job.html"
    form_class = JobForm
    queryset = Job.objects.all()
    success_url = "/jobs/find_a_job"

    def get_object(self):
        """
        Get the current job object to be edited.
        """
        job_id = self.kwargs.get("job_id")
        return get_object_or_404(Job, pk=job_id)

    def get(self, *args, **kwargs):
        """
        Restrict access to Edit Job page only to user who owns the Job object.
        """
        current_job = self.get_object()
        if not current_job.job_poster.user == self.request.user:
            messages.warning(self.request, mark_safe("You cannot browse another member's job."))
            return redirect(reverse("home"))
        return super().get(*args, **kwargs)


    def post(self, request, *args, **kwargs):
        """
        Process the "event_datetime" field of the post request,
        turning it into a python datetime object, interpretable
        by Django.
        """
        
        event_datetime = request.POST.get("event_datetime")
        parsed_datetime = parser.parse(event_datetime)
        request.POST = request.POST.copy()
        request.POST["event_datetime"] = parsed_datetime
     
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Return success message upon successful submission of form.
        """
        messages.success(self.request, "Job form edited")
        return super().form_valid(form)



    
def delete_job(request, job_id):
    """
    Delete Job View
    --------------------

    Gets the job object using the ID passed in url, 
    and deletes it from the table.

    If successful, a success message is displayed, 
    and user is redirected back to the job_list page.

    If unsuccessful, an error message is displayed,
    and user is redirected back to the job_list page.
    """
    current_job = get_object_or_404(Job, pk=job_id)
    try:
        current_job.delete()
        messages.success(request, "Your job was deleted.")
        return redirect(reverse("job_list"))
    except Exception as e:
        messages.error(request, f"Sorry, there was an error: {e}")
        return redirect(reverse("job_list"))


def register_interest(request, job_id, username):
    """
    View to update a given Job object with the profile
    of a user who has sent an offer to do a Job. 
    """
    current_job = get_object_or_404(Job, pk=job_id)
    current_user = get_object_or_404(UserProfile, user__username=username)

    # Restrict access to view to Tier Two members only.
    if not current_user.is_paid:
        messages.warning(request, "You need to be a Tier Two member to make an offer.")
        return redirect(reverse("job_list"))

    current_job.interested_member.add(current_user)
    current_job.interest_count += 1
    current_job.save()

    return redirect(reverse("job_list"))


def confirm_job_offer(request, job_id, confirmed_user_username):
    """
    Handles Booking object creation, when one member confirms another
    on a job they have advertised (Tier Two feature).

    Gets the current job by ID, and both the job poster's profile and
    confirmed member's profile.

    Create a Booking object with a relation to the confirmed job.

    Set the "confirmed_member" attribute of the Job model to the 
    confirmed_user_profile.

    Set the "is_taken" attribute of the Job object to True.
    """
    current_job = get_object_or_404(Job, pk=job_id)
    confirmed_user_profile = get_object_or_404(UserProfile, user__username=confirmed_user_username)
    job_poster_profile = get_object_or_404(UserProfile, user__username=request.user.username)

    # Restrict access to view to the owner of the job object.
    if current_job.job_poster.user != request.user:
        messages.warning(request, "You do not have the authority to be here!")

    try:
        Booking.objects.create(related_job=current_job)
        current_job.confirmed_member = confirmed_user_profile
        current_job.is_taken = True
        current_job.save()
        messages.success(request, f"{confirmed_user_profile.first_name} has been confirmed.")
        return redirect(reverse("dashboard", args=[job_poster_profile.slug]))
    except Exception as e:
        print(f"Exception: {e}")
        messages.error(request, f"Sorry, something went wrong. Please try again.")
        return redirect(reverse("dashboard", args=[job_poster_profile.slug]))

def get_interested_members(request, job_id):
    """
    AJAX Handler to return details of members who have
    registered 
    """
    job = get_object_or_404(Job, pk=job_id)

    if len(job.interested_member.all()) > 0:
        interested_members = []
        member_details = {}
        for member in job.interested_member.all():
            
            members_instruments = []

            if member.first_name or not member.first_name == "":
                member_details["first_name"] = member.first_name
                member_details["last_name"] = member.last_name
            else:
                member_details["username"] = member.user.username
            if member.profile_image:
                member_details["profile_image"] = member.profile_image.url
            if member.city and member.country:
                member_details["city"] = member.city
                member_details["country"] = member.country.name
            member_details["username"] = member.user.username
            member_details["job_id"] = job.pk

            if len(member.instruments_played.all()) > 0:
                for instrument in member.instruments_played.all():
                    members_instruments.append(instrument.instrument_name)
                    member_details["instruments_played"] = members_instruments

            interested_members.append(member_details.copy())
        return JsonResponse({"member_details": interested_members})
