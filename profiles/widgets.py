from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    Custom ClearableFileInput to customize initial
    text, input labels and HTML template.
    """
    clear_checkbox_label = _("Remove")
    initial_text = _("Current Image")
    input_text = _(" ")
    template_name = (
        "profiles/custom_widget_templates/custom_clearable_file_input.html"
    )
