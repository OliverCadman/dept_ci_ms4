from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit


from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:

        model = Message

        fields = ["message"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        placeholders = {
            "message": "Send a message"
        }

        self.fields["message"].widget.attrs["placeholder"] = placeholders["message"]
    
    message = forms.CharField(label="Your message:",
                              widget=forms.TextInput())

