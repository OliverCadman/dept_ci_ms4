from django import forms
from .models import (UserProfile, Instrument,
                     Genre, UnavailableDate, AudioFile, Equipment)
from django_countries.widgets import CountrySelectWidget
from django_countries import Countries



class UserProfileForm(forms.ModelForm):


    class Meta:
        model = UserProfile
        exclude = ("user", "subscription_chosen", "is_paid",)
        widgets = {"country": CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["instruments_played"].initial = [c.pk for c in Instrument.objects.all()]
        self.fields["genres"].initial = [c.pk for c in Genre.objects.all()]

    
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "City"})
    )
    country = forms.ChoiceField(choices=Countries)
    profile_image = forms.ImageField(
        label="Profile Image",
        required=False
    )
    instruments_played = forms.ModelMultipleChoiceField(
        queryset=Instrument.objects.all(),
        label="Which instruments do you play?",
        to_field_name="instrument_name",
        widget=forms.CheckboxSelectMultiple     
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        label="Which genres are you skilled in?",
        to_field_name="genre_name",
        widget=forms.CheckboxSelectMultiple
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment_name"].label = ''

    equipment_name = forms.CharField(
        label="Please list your equipment",
        widget=forms.TextInput
    )


class AudioForm(forms.ModelForm):
    
    class Meta:
        model = AudioFile
        exclude = ("related_user",)

    file=forms.FileField(required=False)

    def save(self, commit=True):
        instance = super(AudioForm, self).save(commit=False)
        file = self["file"].value()

        if commit:
            instance.save()
        return instance

