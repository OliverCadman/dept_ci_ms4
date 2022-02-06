from django import forms
from .models import (UserProfile, Instrument,
                     Genre, UnavailableDate, AudioFile)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ("user", "subscription_chosen", "is_paid",)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "city": "City",
            "country": "Country",
            "instruments_played": "Which instruments do you play?",
            "genres": "Which genres are you skilled in?",
            "user_info": "Tell us about yourself",
        }

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
            else: 
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = "btn dept=form-input"
            self.fields[field].label = False