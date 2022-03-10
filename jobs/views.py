from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

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

        print(self.pre_context)

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
        print("context in dep list view")
        print(context)
        
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

        print(context)
        

        return context

