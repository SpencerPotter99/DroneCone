from rest_framework import serializers
from .models import *

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

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cones = IceCreamConeSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'