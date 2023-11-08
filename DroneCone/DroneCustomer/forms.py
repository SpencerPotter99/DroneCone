from .models import (IceCreamCone)
from django import forms


class IceCreamConeForm(forms.ModelForm):
    class Meta:
        model = IceCreamCone
        fields = ['flavor', 'toppings', 'cone', 'size']
        widgets = {
            'flavor': forms.RadioSelect(),
            'cone': forms.RadioSelect(),
            'size': forms.RadioSelect(),
            'toppings': forms.CheckboxSelectMultiple(),
        }