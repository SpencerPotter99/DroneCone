from django import forms
from DroneCustomer.models import Drone
from decimal import Decimal



class DroneForm(forms.ModelForm):
    battery_percentage = forms.DecimalField(decimal_places=0, min_value=0, max_value=100)

    class Meta:
        model = Drone
        fields = [
            'name',
            'size',
            'drone_weight_g',
            'battery_capacity_mAh',
            'battery_voltage',
            'battery_percentage',
            'enabled',
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.battery_level is not None:
            initial_battery_percentage = (Decimal(self.instance.battery_level) * Decimal(100))
            self.initial['battery_percentage'] = initial_battery_percentage.quantize(Decimal(1))

    def save(self, commit=True, kwargs=None):
        model = super(forms.ModelForm, self).save(commit=False)

        battery_percentage = self.cleaned_data.get('battery_percentage')
        model.battery_level = battery_percentage / Decimal(100)

        if commit:
            model.save()
        return model