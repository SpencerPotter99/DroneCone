from django import forms
from DroneCustomer.models import Drone, IceCream, Topping, Cone

class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = [
            'name',
            'size',
            'drone_weight_g',
            'battery_capacity_mAh',
            'battery_voltage',
            'battery_level',
            'enabled',
            'in_flight'
        ]

class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['flavor', 'description', 'price', 'qty']

class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name', 'description', 'price', 'qty']

class ConeForm(forms.ModelForm):
    class Meta:
        model = Cone
        fields = ['name', 'description', 'price', 'qty']
