from django import forms
from DroneCustomer.models import Drone

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