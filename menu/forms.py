from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    """
    Form for creating and updating menu items.

    This form is based on the MenuItem model and includes fields for
    'name', 'description', 'price', 'category', and 'image'.

    Attributes:
    - model: MenuItem
    - fields: ['name', 'description', 'price', 'category', 'image']
    
    """
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'image']
