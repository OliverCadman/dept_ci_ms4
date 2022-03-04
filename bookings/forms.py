from django import forms
from django_countries import Countries
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML
from crispy_forms.bootstrap import PrependedText

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Booking, Invitation
from profiles.models import UserProfile



class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        exclude = ("invite_sender", "invite_receiver",
                   "is_accepted", "date_of_invitation")


    def __init__(self, *args, **kwargs):
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

        self.helper["fee"].wrap(PrependedText, mark_safe("<i class='fas fa-pound-sign'></i>"))

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

    class Meta:
        model = Booking
        exclude = ("related_invitation",)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    travel_provided = forms.ChoiceField(label="Is Travel Provided?",
                                          widget=forms.CheckboxInput)

    travel_info = forms.CharField(label="What are the travel plans?",
                                  widget=forms.Textarea(attrs={
                                      "rows": "3"
                                  }))

    backline_provided = forms.ChoiceField(label="Is backline provided?",
                                          widget=forms.CheckboxInput)

    backline_info = forms.CharField(label="What equipment is provided?",
                                    widget=forms.Textarea(attrs={
                                        "rows": "2"
                                    }))


    


    
    

    


    