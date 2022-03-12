from django import forms
from django.forms import ValidationError
from .models import (UserProfile, Instrument,
                     Genre, UnavailableDate, AudioFile, Equipment)
from django_countries.widgets import CountrySelectWidget
from django_countries import Countries

from .widgets import CustomClearableFileInput

import os



class UserProfileForm(forms.ModelForm):


    class Meta:
        model = UserProfile
        exclude = ("user", "subscription_chosen",
                   "invitation_count, ""is_paid",)
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
        required=False,
        widget=CustomClearableFileInput
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
        widget=forms.TextInput,
        required=False
    )


class AudioForm(forms.ModelForm):
    
    class Meta:
        model = AudioFile
        exclude = ("related_user", "related_booking", "file_name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["file"].label = ""

    file=forms.FileField(required=False, widget=forms.FileInput(
        attrs={"class": "custom-formfield-font"}
    ))

    def clean_file(self):
        """
        Validate file size and extension of audio files.
        """

        # Filesize Validation (5MB Limit)
        filesize_limit = 5 * 1024 * 1024
        data = self.cleaned_data["file"]
        print("DATA")
        print(data)
        if data:
            if data.size > filesize_limit:
                raise ValidationError("Please submit a file less than 5MB.")

            # File extension validation
            allowed_extensions = list(os.environ.get("ALLOWED_AUDIOFILE_EXTENSIONS").split(","))
            allowed_extensions = [x.strip(" ") for x in allowed_extensions]
            filename, file_extension = os.path.splitext(data.name)
            print("filename")
            print(filename)
            print(file_extension)
            if filename != '':
                if file_extension not in allowed_extensions:
                    raise ValidationError("Only mp3, mp4, m4a, wav, aac, and flac files are supported.")
                return data

    def save(self, commit=True):
        instance = super(AudioForm, self).save(commit=False)
        file = self["file"].value()

        if commit:
            instance.save()
        return instance

