from django import forms
from django_countries.fields import CountryField
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, ButtonHolder, Submit
from crispy_forms.bootstrap import PrependedText

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Job


class JobForm(forms.ModelForm):
    """
    Form to Post a Job Advertisement
    """

    class Meta:
        """
        Declare model to manipulate, and which fields to exclude.
        """
        model = Job
        exclude = ("job_poster", "interested_member", "interest_count",
                   "is_taken")
    
    def __init__(self, *args, **kwargs):
        """
        Crispy Form Helper to Design layout, and allow
        for prepended currency icon in "Fee" field.

        Add classname "secondary_font" to all fields.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "/jobs/post_job"
        self.helper.form_method = "post"
        self.helper.form_id = "job_post_form"
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
                        css_class="custom_success secondary_font inset_light_shadow"
                    )
                ), css_class="row"
            )
        )


        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "secondary_font"

        # Prepend Pound sign icon to "Fee" Field
        self.helper["fee"].wrap(PrependedText, mark_safe("<i class='fas fa-pound-sign'></i>"))

    job_title = forms.CharField(label="Who are you looking for?",
                                widget=forms.TextInput(attrs={
                                    "placeholder": "Keys player required. Urgent!"
                                }))

    event_name = forms.CharField(label="What is your event?",
                                 widget=forms.TextInput(attrs={
                                     "placeholder": "Late Show at Ronnie Scotts"
                                 }))
    artist_name = forms.CharField(label="For which artist?",
                                  widget=forms.TextInput(attrs={
                                      "placeholder": "Ariana Grande"
                                  }))
    job_description = forms.CharField(label="What does the job involve?",
                                      widget=forms.Textarea(attrs={
                                          "placeholder": "Need someone with good knowledge of synthesizers",
                                          "rows": "4"
                                      }))
    fee = forms.DecimalField(widget=forms.NumberInput(attrs={
                                "placeholder": "150"
                            }))

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
