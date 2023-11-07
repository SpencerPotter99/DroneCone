from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import IceCream, IceCreamCone, Topping, Cone, Order
from .serializers import *

class MenuItemsAPI(APIView):
    def get(self, request):
        menu_items = IceCream.objects.all()
        serializer = IceCreamSerializer(menu_items, many=True)
        print(menu_items)
        return Response(serializer.data)

class ToppingsItemsAPI(APIView):
    def get(self, request):
        topping_items = Topping.objects.all()
        serializer = ToppingSerializer(topping_items, many=True)
        print(topping_items)
        return Response(serializer.data)

class ConeItemsAPI(APIView):
    def get(self, request):
        cone_items = Cone.objects.all()
        serializer = ConeSerializer(cone_items, many=True)
        print(cone_items)
        return Response(serializer.data)

class IceCreamConeCreateView(generics.CreateAPIView):
    queryset = IceCreamCone.objects.all()
    serializer_class = IceCreamConeSerializer

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # Get the currently logged-in user
        return Order.objects.filter(user=user)

class CartView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        return self.request.user.cart

class GetUserIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        return Response({'user_id': user_id})

class AddToCartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cone_id = self.request.data.get('cone_id')  # Assuming you send the cone_id in the request data
        try:
            cone = IceCreamCone.objects.get(pk=cone_id)
        except IceCreamCone.DoesNotExist:
            return Response({'detail': 'Cone not found.'}, status=status.HTTP_NOT_FOUND)
        user.cart.cones.add(cone)
        serializer.save(user=user)


def index(request):
    return render(request, 'DroneCustomer/index.html')

def home(request):
    return render(request, 'DroneCustomer/home.html')

def checkout(request):
    return render(request, 'DroneCustomer/checkout.html')

def account(request):
    return render(request, 'DroneCustomer/account.html')

# def login(request):
#     return render(request, 'Account/login.html')

def droneManagement(request):
    return render(request, 'DroneCustomer/droneManager.html')

def droneOwnerCreation(request):
    return render(request, 'DroneCustomer/droneOwnerCreation.html')

def signUp(request):
    return render(request, 'DroneCustomer/customerCreation.html')

def editAccount(request):
    return render(request, 'DroneCustomer/editAccount.html')
