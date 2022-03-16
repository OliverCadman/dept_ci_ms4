from django import forms
from django.forms import ValidationError
from django_countries import Countries
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML
from crispy_forms.bootstrap import PrependedText


from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Booking, Invitation, Review

import re


class InvitationForm(forms.ModelForm):
    """
    Invitation Form

    Collects details of a gig/event that a member is
    inviting another member to play.
    """

    class Meta:
        """
        Define the form 'Meta' properties
        """
        model = Invitation
        exclude = ("invite_sender", "invite_receiver",
                   "is_accepted", "date_of_invitation")


    def __init__(self, *args, **kwargs):
        """
        Add placeholders and instantiate Crispy Helper
        to aide with layout.
        """
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "/bookings/invite"
        self.helper.form_method = "post"
        self.helper.form_id = "invitation_form"
        self.helper.add_input(Submit('submit', "Submit"))
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML("<h2 class='form-header'>Invite {% if user.first_name %}{{user.first_name}}{% else %}{{ user.user.username }}{% endif %} to your gig.</h2>"),
                    "event_name",
                    "artist_name",
                    "event_city",
                    "event_country",
                    "event_datetime",
                    "fee",
                    "additional_info"
                )
            )
        )

        # Bootstrap prepend the "fee" field with a currency icon
        self.helper["fee"].wrap(PrependedText, mark_safe("<i class='fas fa-pound-sign'></i>"))

        # Define placeholders
        placeholders = {
        "event_name": "Headline slot at O2 Academy...",
        "artist_name": "The Mars Volta, Radiohead...",
        "event_city": "Manchester",
        "fee": 150,
        "event_datetime": "27/04/2021 14:00",
        "additional_info": "90 minute set, charts provided..."
        }

        excluded_placeholders = ["event_country"]

        for field in self.fields:
            if field not in excluded_placeholders:
                placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "custom-formfield-font"

    def clean_event_name(self):
        """
        Raise a validation error if event_name field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        event_name = self.cleaned_data["event_name"]
        regex = "^[0-9]+$"
        if re.match(regex, event_name):
            raise ValidationError("Please enter words as well as numbers.", code="invalid")
        else:
            return event_name

    
    def clean_artist_name(self):
        """
        Raise a validation error if artist_name field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        artist_name = self.cleaned_data["artist_name"]
        regex = "^[0-9]+$"
        if re.match(regex, artist_name):
            raise ValidationError("Please enter words as well as numbers.", code="invalid")
        else:
            return artist_name

    def clean_event_city(self):
        """
        Raise a validation error if event_city field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        event_city = self.cleaned_data["event_city"]
        regex= "^[0-9]+$"
        if re.match(regex, event_city):
            raise ValidationError("Please enter words as well as numbers.")
        else:
            return event_city

    def clean_additional_info(self):
        """
        Raise a validation error if additional_info field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        additional_info = self.cleaned_data["additional_info"]
        regex = "^[0-9]+$"
        if re.match(regex, additional_info):
            raise ValidationError("Please enter words as well as numbers.")
        else:
            return additional_info


    # Create widgets for inputs
    event_name = forms.CharField(
        label="The name of your event",
        widget=forms.TextInput()
    )

    artist_name = forms.CharField(
        label="The name of the artist/band",
        widget=forms.TextInput()
    )

    event_city = forms.CharField(
        label="The city where the event is taking place",
        widget=forms.TextInput()
    )

    event_country = forms.ChoiceField(choices=Countries)

    event_datetime = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M:%S"],
        label="Date and Time of your Event",
        widget=DateTimePickerInput(format=("%d-%m-%Y %H:%M:%S"), attrs={
            "id": "date_time_picker"
        }),

    )

    fee = forms.DecimalField(
        widget=forms.NumberInput()
    )

    additional_info = forms.CharField(
        label="Any additional info?",
        required=False,
        widget=forms.Textarea(attrs={
            "rows": "3",
        })
    )


class BookingForm(forms.ModelForm):
    """
    Booking Form

    Available once a member has accepted another member's
    invitation.

    Used to collect further details of an engagement, with 
    all other details persisting from the model created from
    the Invitation form.
    """

    class Meta:
        """
        Define the "Meta" properties of the form.
        """
        model = Booking
        exclude = ("related_invitation", "related_job",)
    

    # Define form widgets.
    venue_name = forms.CharField(label="Name of the Venue",
                                 widget=forms.TextInput)
    
    street_address1 = forms.CharField(label="Street Address 1",
                                 widget=forms.TextInput)

    street_address2 = forms.CharField(label="Street Address 2",
                                 widget=forms.TextInput,
                                 required=False)

    postcode = forms.CharField(label="Postcode/ZIP",
                               widget=forms.TextInput,
                               required=False)


    travel_provided = forms.BooleanField(label="Is Travel Provided?",
                                        required=False,
                                        widget=forms.CheckboxInput)

    travel_info = forms.CharField(label="What are the travel plans?",
                                  required=False,
                                  widget=forms.Textarea(attrs={
                                      "rows": "3"
                                  }))

    backline_provided = forms.BooleanField(label="Is backline provided?",
                                          required=False,
                                          widget=forms.CheckboxInput

                                          )

    backline_info = forms.CharField(label="What equipment is provided?",
                                    required=False,
                                    widget=forms.Textarea(attrs={
                                        "rows": "2"
                                    }))


class ReviewForm(forms.ModelForm):
    """
    Review Form

    Enables a user to leave a review for another user.
    """
     
    class Meta:
        """
        Define "Meta" properties of the form.
        """
        model = Review
        exclude = ("related_booking", "review_sender", "review_receiver",
                "review_created", "review_modified",)
    


    def __init__(self, *args, **kwargs):
        """
        Remove label for "review_content"
        """
        super().__init__(*args, **kwargs)
        
        self.fields["review_content"].label = ""
        
    
    # Define form widgets
    review_content = forms.CharField(label="Leave your review",
                                     widget=forms.Textarea(attrs={
                                         "placeholder": "Tell the community what you think"
                                     }))

    # Hidden input value is determined by "star" rating, inputted through JavaScript.
    rating = forms.IntegerField(widget=forms.HiddenInput)
