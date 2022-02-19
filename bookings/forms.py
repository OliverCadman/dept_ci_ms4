from django import forms
from django_countries import Countries
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, Fieldset, HTML
from crispy_forms.bootstrap import PrependedText

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Invitation
from profiles.models import UserProfile



class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        exclude = ("invite_sender", "invite_receiver",
                   "is_accepted", "date_of_invitation")


    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "invite"
        self.helper.form_method = "post"
        self.helper.form_id = "invitation_form"
        self.helper.add_input(Submit('submit', "Submit"))
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML("<h2>Invite {{user.first_name}} to your gig.</h2>"),
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
        label="Date and Time of your Event",
        widget=DateTimePickerInput(format="%d/%m/%Y %H:%M")
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

    
    

    


    