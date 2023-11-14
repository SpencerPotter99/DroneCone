
from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import IceCream, IceCreamCone, Topping, Cone, Order
from .serializers import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from .forms import DroneForm


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
    
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):
        try:
            # Retrieve the order with the specified order_id
            order = Order.objects.get(pk=order_id)

            # Update the order status to "Delivered"
            order.status = 'delivered'
            order.save()

            return Response({'message': 'Order status updated to "Delivered".'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error updating order status.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cones']

def index(request):
    return render(request, 'DroneCustomer/index.html')

def home(request):
    return render(request, 'DroneCustomer/home.html')


@login_required
def checkout(request):
    user = request.user
    # Get all orders for the current user with 'pending' status
    pending_orders = Order.objects.filter(user=user, status='pending')

    order_items = []
    total_price = Decimal('0.00')

    # Iterate over pending orders to collect order items and compute the total price
    for order in pending_orders:
        cones_info = order.get_cone_info()
        order_items.extend(cones_info)
        total_price += order.get_order_total()

    context = {
        'order_items': order_items,
        'total_price': total_price,
    }
    return render(request, 'DroneCustomer/checkout.html', context)


@login_required
def account(request):
    user = request.user
    total_orders = Order.objects.filter(user=user).count()
    orders = Order.objects.filter(user=user).order_by('-created_at')

    # Define delivery duration as 10 minutes
    delivery_duration = timedelta(minutes=10)

    # Go through orders and calculate remaining delivery time
    for order in orders:
        if order.status == 'delivering':
            # Time since the order was last updated
            time_since_update = timezone.now() - (timezone.now() - timezone.timedelta(minutes=5))

            # Remaining delivery time is the delivery duration minus the time since last update
            remaining_time = delivery_duration - time_since_update

            # If the remaining time is negative, delivery should have been completed
            remaining_time_seconds = max(remaining_time.total_seconds(), 0)

            # Add remaining time in seconds to the order object for use in the template
            order.remaining_delivery_time_seconds = int(remaining_time_seconds)
        else:
            # If the order is not delivering, set remaining time to None
            order.remaining_delivery_time_seconds = None

    context = {
        'total_orders': total_orders,
        'orders': orders,
    }
    return render(request, 'DroneCustomer/account.html', context)


def droneManagement(request):
    return render(request, 'DroneCustomer/droneManager.html')

def droneOwnerCreation(request):
    return render(request, 'DroneCustomer/droneOwnerCreation.html')

def signUp(request):
    return render(request, 'DroneCustomer/customerCreation.html')

@login_required
def editAccount(request):
    user = request.user
    email = user.email
    profile = user.profile
    context = {
        'profile': profile,
        'email': email
    }
    return render(request, 'DroneCustomer/editAccount.html', context)


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
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        drone_owner = request.POST.get('drone_owner') == 'on'

        user = request.user

        # Verify the current password
        if current_password:
            if not user.check_password(current_password):
                messages.error(request, 'Incorrect current password.')
                return redirect('editaccount')

        # Update user email
        if email:
            user.email = email

        # Update profile address and phone
        user.profile.address = address
        user.profile.phone = phone
        user.profile.drone_owner = drone_owner

        # Update drone owner status
        user.profile.drone_owner = drone_owner

        # Save the profile changes
        user.profile.save()

        # Change password if provided
        if new_password and confirm_password:
            if new_password == confirm_password:
                user.set_password(new_password)  # Use set_password instead of directly assigning
                update_session_auth_hash(request, user)  # Update session with the new password
                user.save()
                messages.success(request, 'Your password has been updated.')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('editaccount')

        # Save the user changes
        user.save()

        messages.success(request, 'Your account has been updated.')
        return redirect('../account/')

    return redirect('editaccount')
    
@login_required
def manageMyDrone(request):
    user_drones = Drone.objects.filter(owner=request.user)
    return render(request, "DroneCustomer/manageMyDrone.html", {'user_drones': user_drones})

@login_required
def customer_add_drone(request, item_id=None):
    if item_id:
        drone = get_object_or_404(Drone, pk=item_id)
        action_title = "Edit"
    else:
        drone = None
        action_title = "Add"
    if request.method == 'POST':
        form = DroneForm(request.POST, instance=drone)
        if form.is_valid():
            form.save()
            return redirect('manageMyDrone')
    else:
        form = DroneForm(instance=drone)
    
    return render(request, 'DroneCustomer/customer_add_drone.html', {'form': form, 'action_title': action_title})

def customer_delete_drone(request, item_id=None):
    if item_id:
        user_drone = get_object_or_404(Drone, pk=item_id)
    else:
        user_drone = None
    if request.method == 'POST':
        user_drone.delete()
        return redirect('manageMyDrone')
    return render(request, 'DroneCustomer/customer_delete_drone', {'user_drone': user_drone})


