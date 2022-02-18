from django import forms
from django_countries import Countries
from .models import Invitation
from profiles.models import UserProfile


class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        exclude = ("invite_sender", "invite_receiver",
                   "is_accepted", "date_of_invitation")

    event_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Please enter the name of your event"
        })
    )

    event_city = forms.CharField(
        widget=forms.TextInput(attrs={
               "placeholder": "The town/city where the event is taking place"
        })
    )

    event_country = forms.ChoiceField(choices=Countries)

    event_datetime = forms.DateTimeField(
        widget=forms.SplitDateTimeWidget()
    )

    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": "3",
            "placeholder": "Additional Information about your event"
        })
    )


    