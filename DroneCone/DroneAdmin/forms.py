from django import forms
from DroneCustomer.models import Drone, IceCream, Topping, Cone
from decimal import Decimal


class CustomNumberInput(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'border border-gray-400 rounded'})
        super().__init__(*args, **kwargs)


class DroneForm(forms.ModelForm):
    battery_level = forms.DecimalField(
        max_value=Decimal('1.0'),
        min_value=Decimal('0.0'),
        widget=CustomNumberInput(),  # Use the custom widget with border style
    )

    class Meta:
        model = Drone
        fields = [
            'owner',
            'name',
            'size',
            'drone_weight_g',
            'battery_capacity_mAh',
            'battery_voltage',
            'battery_level',
            'enabled',
            'in_flight'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'drone_weight_g': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
            'battery_capacity_mAh': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
            'battery_voltage': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'border border-gray-400 rounded'}),
            'in_flight': forms.CheckboxInput(attrs={'class': 'border border-gray-400 rounded'}),
        }


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['flavor', 'price', 'qty']
        widgets = {
            'flavor': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'price': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
            'qty': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
        }


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name', 'price', 'qty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'price': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
            'qty': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
        }


class ConeForm(forms.ModelForm):
    class Meta:
        model = Cone
        fields = ['name', 'price', 'qty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'price': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
            'qty': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded'}),
        }
