from attr import attr
from django import forms
from .models import (UserProfile, Instrument,
                     Genre, UnavailableDate, AudioFile, Equipment)
from .widgets import EquipmentTextWidget


class UserProfileForm(forms.ModelForm):


    class Meta:
        model = UserProfile
        exclude = ("user", "subscription_chosen", "is_paid",)


    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )

    city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "City"})
    )

    country = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Country"}
        )
    )

    profile_image = forms.ImageField(
        label="Profile Image",
        required=False
    )

    instruments_played = forms.ModelMultipleChoiceField(
        queryset=Instrument.objects.all(),
        label="Which instruments do you play?",
        
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        label="Which genres are you skilled in?"
    )

    user_info = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",
                "placeholder": "Tell us about yourself!"
            }
        )
    )


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        exclude = ("related_user",)

    
    class Media:
         js = ("profiles/js/equipment_text_input.js",)

    equipment_name = forms.CharField(
        label="Please list your equipment",
        widget=forms.TextInput()
    )


