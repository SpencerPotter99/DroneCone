from rest_framework import serializers
from .models import IceCream, IceCreamCone, Topping, Cone

class IceCreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceCream
        fields = '__all__'

class ConeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cone
        fields = '__all__'
class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = '__all__'
class IceCreamConeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceCreamCone
        fields = '__all__'