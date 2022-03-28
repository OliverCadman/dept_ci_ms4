from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit

from .models import Message


class MessageForm(forms.ModelForm):
    """
    Message Form
    -------------------

    Provides a form for a User to send a message
    to another user.
    """
    class Meta:
        """
        Define the META attributes of the form.
        """
        model = Message

        fields = ["message"]

    def __init__(self, *args, **kwargs):
        """
        Provide custom placeholders and classes to message field
        """
        super(MessageForm, self).__init__(*args, **kwargs)

        placeholders = {
            "message": "Send a message"
        }

        self.fields["message"].widget.attrs["placeholder"] = (
            placeholders["message"])
        self.fields["message"].widget.attrs["class"] = (
            "custom-formfield-font")
        self.fields["message"].label = ""

    # Define message field widget
    message = forms.CharField(widget=forms.TextInput())
