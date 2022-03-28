from django import forms
from django_countries.fields import CountryField
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, ButtonHolder, Submit
from crispy_forms.bootstrap import PrependedText
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Job
from profiles.widgets import CustomClearableFileInput

import re


class JobForm(forms.ModelForm):
    """
    Form to Post a Job Advertisement
    """

    class Meta:
        """
        Declare model to manipulate, and which fields to exclude.
        """
        model = Job
        exclude = ("job_poster", "interested_member",
                   "interest_count", "is_taken")

    def __init__(self, *args, **kwargs):
        """
        Crispy Form Helper to Design layout, and allow
        for prepended currency icon in "Fee" field.

        Add classname "secondary_font" to all fields.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    "job_title",
                    css_class="col-12"
                ),
                Div(
                    "event_name",
                    css_class="col-12 col-md-6"
                ),
                Div(
                    "artist_name",
                    css_class="col-12 col-md-6"
                ),
                Div(
                    "job_description",
                    css_class="col-12"
                ),
                Div(
                    "fee",
                    css_class="col-12 col-md-6"
                ),
                Div(
                    "image",
                    css_class="col-12 col-md-6"
                ),
                Div(
                    "event_city",
                    css_class="col-12 col-md-6",
                ),
                Div(
                    "event_country",
                    css_class="col-12 col-md-6"
                ),
                Div(
                    "event_datetime",
                    css_class="col-12 col-md-6"
                ),
                ButtonHolder(
                    Submit(
                        "submit",
                        "Submit",
                        css_class="custom_success secondary_font"
                                  " inset_light_shadow"
                    )
                ), css_class="row"
            )
        )

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "secondary_font"

        # Prepend Pound sign icon to "Fee" Field
        self.helper["fee"].wrap(PrependedText, mark_safe(
            "<i class='fas fa-pound-sign'></i>"))

    def clean_job_title(self):
        """
        Raise a validation error if job_title
        field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        job_title = self.cleaned_data["job_title"]
        regex = "^[0-9]+$"
        if re.match(regex, job_title):
            raise forms.ValidationError(
                "Please enter words as well as numbers.", code="invalid")
        else:
            return job_title

    def clean_event_name(self):
        """
        Raise a validation error if event_name field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        event_name = self.cleaned_data["event_name"]
        regex = "^[0-9]+$"
        if re.match(regex, event_name):
            raise forms.ValidationError(
                "Please enter words as well as numbers.", code="invalid")
        else:
            return event_name

    def clean_artist_name(self):
        """
        Raise a validation error if artist_name field
        consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        artist_name = self.cleaned_data["artist_name"]
        regex = "^[0-9]+$"
        if re.match(regex, artist_name):
            raise forms.ValidationError(
                "Please enter words as well as numbers.", code="invalid")
        else:
            return artist_name

    def clean_job_description(self):
        """
        Raise a validation error if job_description
        field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        job_description = self.cleaned_data["job_description"]
        regex = "^[0-9]+$"
        if re.match(regex, job_description):
            raise forms.ValidationError(
                "Please enter words as well as numbers.", code="invalid")
        else:
            return job_description

    def clean_event_city(self):
        """
        Raise a validation error if event_city
        field consists of only numbers.

        Uses regex pattern to compare against input's value.
        """
        event_city = self.cleaned_data["event_city"]
        regex = "^[0-9]+$"
        if re.match(regex, event_city):
            raise forms.ValidationError(
                "Please enter words as well as numbers.", code="invalid")
        else:
            return event_city

    job_title = forms.CharField(
        label="Who are you looking for?",
        widget=forms.TextInput(attrs={
                "placeholder": "Keys player required. Urgent!"
            }))

    event_name = forms.CharField(
        label="What is your event?",
        widget=forms.TextInput(attrs={
                "placeholder": "Late Show at Ronnie Scotts"
            }))
    artist_name = forms.CharField(label="For which artist?",
                                  widget=forms.TextInput(attrs={
                                      "placeholder": "Ariana Grande"
                                  }))

    job_description = forms.CharField(
        label="What does the job involve?",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Need someone with a good soul repertoire",
                "rows": "4"
            }))
    fee = forms.DecimalField(widget=forms.NumberInput(attrs={
                                "placeholder": "150"
                            }))

    image = forms.ImageField(required=False, widget=CustomClearableFileInput)

    event_city = forms.CharField(label="Where is the event taking place?",
                                 widget=forms.TextInput(attrs={
                                     "placeholder": "Birmingham, New York..."
                                 }))

    event_country = CountryField()

    event_datetime = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M:%S"],
        label="Date and Time of your Event",
        widget=DateTimePickerInput(format=("%d-%m-%Y %H:%M:%S"), attrs={
            "id": "date_time_picker",
        }),
    )
