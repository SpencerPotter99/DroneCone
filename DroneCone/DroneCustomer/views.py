from django.shortcuts import render
from .models import Order
# Create your views here.
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import IceCream, IceCreamCone, Topping, Cone
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

class OrderCreateView(APIView):
    def post(self, request):
        print("TEST")
        serializer = IceCreamConeSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assuming you have user authentication
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    return render(request, 'DroneCustomer/index.html')

def home(request):
    return render(request, 'DroneCustomer/home.html')

def checkout(request):
    return render(request, 'DroneCustomer/checkout.html')



def account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'DroneCustomer/account.html', context)

def login(request):
    return render(request, 'DroneCustomer/login.html')

def droneManagement(request):
    return render(request, 'DroneCustomer/droneManager.html')

def droneOwnerCreation(request):
    return render(request, 'DroneCustomer/droneOwnerCreation.html')

def signUp(request):
    return render(request, 'DroneCustomer/customerCreation.html')

def editAccount(request):
    return render(request, 'DroneCustomer/editAccount.html')
