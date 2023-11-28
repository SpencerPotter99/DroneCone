from django import forms
from django.contrib.auth.models import User
# noinspection PyUnresolvedReferences
from DroneCustomer.models import Drone, IceCream, Topping, Cone, Markup
# noinspection PyUnresolvedReferences
from Account.models import Profile
from decimal import Decimal


class MarkupForm(forms.ModelForm):
    class Meta:
        model = Markup
        fields = ['markup_percentage']

        widgets = {
            'markup_percentage': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'})
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'phone', 'address', 'drone_owner']

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'address': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'drone_owner': forms.CheckboxInput(attrs={'class': 'border border-gray-400 rounded'}),
        }

class CustomNumberInput(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'border border-gray-400 rounded text-right'})
        super().__init__(*args, **kwargs)

class DroneForm(forms.ModelForm):
    battery_level = forms.DecimalField(
        max_value=Decimal('1.0'),
        min_value=Decimal('0.0'),
        widget=CustomNumberInput(),
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
            'drone_weight_g': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
            'battery_capacity_mAh': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
            'battery_voltage': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'border border-gray-400 rounded'}),
            'in_flight': forms.CheckboxInput(attrs={'class': 'border border-gray-400 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(profile__drone_owner=True)

class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['flavor', 'price', 'qty']
        widgets = {
            'flavor': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'price': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
            'qty': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
        }

class BaseForm(forms.ModelForm):
    class Meta:
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-400 rounded'}),
            'price': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
            'qty': forms.NumberInput(attrs={'class': 'border border-gray-400 rounded text-right'}),
        }

class ToppingForm(BaseForm):
    class Meta:
        model = Topping
        fields = ['name', 'price', 'qty']

class ConeForm(BaseForm):
    class Meta:
        model = Cone
        fields = ['name', 'price', 'qty']