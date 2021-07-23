from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Ability to add, update and delete products

    """

    class Meta:
        # defines model and fields to include
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        # override the init method
        # to make changes to fields
        super().__init__(*args, **kwargs)

        # get cateogries to show in their friendly name
        categories = Category.objects.all()
        # list comprehension for loop to get friendly names
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # use category friendly name instead of id
        self.fields['category'].choices = friendly_names

        # iterate through fields with css for consistency
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
 