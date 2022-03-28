from django import forms
from django.forms import ValidationError
from .models import (UserProfile, Instrument,
                     Genre, UnavailableDate, AudioFile, Equipment)
from django_countries.widgets import CountrySelectWidget
from django_countries import Countries

from .widgets import CustomClearableFileInput

import os


class UserProfileForm(forms.ModelForm):
    """
    UserProfileForm
    ---------------------

    Collect a user's personal information
    to be displayed on their profile page.
    """

    class Meta:
        """
        Define the Meta Properties of the
        UserProfile Form.
        """
        model = UserProfile
        exclude = ("user", "subscription_chosen",
                   "invitation_count", "is_paid",)
        widgets = {"country": CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        """
        Inject the 'instruments_played' and 'genres' M2M field values
        with their IDs.
        """
        super().__init__(*args, **kwargs)
        self.fields["instruments_played"].initial = (
            [c.pk for c in Instrument.objects.all()])
        self.fields["genres"].initial = [c.pk for c in Genre.objects.all()]

    # Define the widgets for form fields
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
    """
    EquipmentForm
    --------------------

    Collect details of user's equipment
    to be displayed on their profile page.
    """

    class Meta:
        """
        Define the META attributes
        """
        model = Equipment
        exclude = ("related_user",)

    def __init__(self, *args, **kwargs):
        """
        Remove the label content for equipment name field
        """
        super().__init__(*args, **kwargs)
        self.fields["equipment_name"].label = ''

    # Define the form's widgets
    equipment_name = forms.CharField(
        label="Please list your equipment",
        widget=forms.TextInput,
        required=False
    )


class AudioForm(forms.ModelForm):
    """
    AudioForm
    -----------------------

    Collects Audio Files relating to a user or booking.

    Used in both the Edit Profile Page and the Booking Page.
    """
    class Meta:
        """
        Define the META properties of the form.
        """
        model = AudioFile
        exclude = ("related_user", "related_booking", "file_name",)

    def __init__(self, *args, **kwargs):
        """
        Remove label text content
        """
        super().__init__(*args, **kwargs)

        self.fields["file"].label = ""

    file = forms.FileField(required=False, widget=forms.FileInput(
        attrs={"class": "custom-formfield-font"}
    ))

    def clean_file(self):
        """
        Validate file size and extension of audio files.

        Files can be no larger than 5MB

        Only mp3, mp4, m4a, wav, aac and flac files are permitted.
        """

        # Filesize Validation (5MB Limit)
        filesize_limit = 5 * 1024 * 1024
        data = self.cleaned_data["file"]
        if data:
            if data.size > filesize_limit:
                raise ValidationError("Please submit a file less than 5MB.")

            # File extension validation
            allowed_extensions = list(
                os.environ.get("ALLOWED_AUDIOFILE_EXTENSIONS").split(","))
            allowed_extensions = [x.strip(" ") for x in allowed_extensions]

            filename, file_extension = os.path.splitext(data.name)
            if filename != '':
                if file_extension not in allowed_extensions:
                    raise ValidationError(
                        "Only mp3, mp4, m4a, wav, aac, "
                        "and flac files are supported.")
                return data

    def save(self, commit=True):
        """
        Custom save method in attempt overcome bug that was
        encountered upon initially testing the
        AudioForm.
        """
        instance = super(AudioForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
