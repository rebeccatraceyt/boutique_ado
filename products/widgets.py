from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
# using 'as _' means you can call gettext_lazy using _()
# creates an alias for convienience

class CustomClearableFileInput(ClearableFileInput):
    # override the following with our own values:
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
