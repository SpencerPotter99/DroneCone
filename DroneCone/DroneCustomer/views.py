from django.shortcuts import render, redirect
from .models import Order
from django import forms
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import IceCream, IceCreamCone, Topping, Cone, Cart
from .serializers import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password


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

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cones']

def index(request):
    return render(request, 'DroneCustomer/index.html')

def home(request):
    return render(request, 'DroneCustomer/home.html')

def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()  # Get the cart for the current user

    if cart is not None:
        order_items = cart.get_cones_info()
        total_price = sum(item['price'] for item in order_items)
    else:
        order_items = []
        total_price = 0

    context = {
        'order_items': order_items,
        'total_price': total_price,
    }

    return render(request, 'DroneCustomer/checkout.html', context)


def account(request):
    user = request.user
    total_orders = Order.objects.filter(user=user).count()
    orders = Order.objects.filter(user=user).order_by('-created_at')

    context = {
        'total_orders': total_orders,
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

def submit_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None or not cart.cones.exists():
        return redirect('some-page')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cones = cart.get_cones_info()  # Assuming the cones data is JSON serializable
            order.save()
            cart.remove_all_cones()  # Clear the cart after order is placed
            return redirect('order-success-page')
    else:
        form = OrderForm()

    return render(request, 'submit_order.html', {'form': form})


def update_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        drone_owner = request.POST.get('drone_owner') == 'on'

        user = request.user

        # Verify the current password
        if not user.check_password(current_password):
            messages.error(request, 'Incorrect current password.')
            return redirect('edit_account')

        if email:
            user.email = email

        if new_password and confirm_password:
            if new_password == confirm_password:
                user.password = make_password(new_password)
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('edit_account')

        user.profile.drone_owner = drone_owner
        user.profile.save()
        user.save()

        update_session_auth_hash(request, user)  # Important, to update the session with the new password
        messages.success(request, 'Your account has been updated.')
        return redirect('account_view')

    return redirect('edit_account')
