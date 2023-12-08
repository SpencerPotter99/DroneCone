
from datetime import timedelta
import decimal
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
from .serializers import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from .forms import DroneForm
from .customerDecorators import drone_owner_required
import threading
from .models import IceCream, Topping, Cone
from django.db.models import Sum, Avg



class MenuItemsAPI(APIView):
    def get(self, request):
        menu_items = IceCream.objects.all()
        serializer = IceCreamSerializer(menu_items, many=True)
        return Response(serializer.data)

class ToppingsItemsAPI(APIView):
    def get(self, request):
        topping_items = Topping.objects.all()
        serializer = ToppingSerializer(topping_items, many=True)
        return Response(serializer.data)

class ConeItemsAPI(APIView):
    def get(self, request):
        cone_items = Cone.objects.all()
        serializer = ConeSerializer(cone_items, many=True)
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
        user = self.request.user
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

@login_required
def home(request):
    return render(request, 'DroneCustomer/home.html')


@login_required
def checkout(request):
    user = request.user
    # Get all orders for the current user with 'pending' status
    pending_orders = Order.objects.filter(user=user, status='pending')
    address = user.profile.address

    order_items = []
    total_price = Decimal('0.00')

    # Iterate over pending orders to collect order items and compute the total price
    for order in pending_orders:
        cones_info = order.get_cone_info()
        for cone in cones_info:
            cone['order_id'] = order.id  # Add order ID to each cone item
            order_items.append(cone)
        total_price += order.get_order_total()

    context = {
        'address': address,
        'order_items': order_items,
        'total_price': total_price,
    }
    return render(request, 'DroneCustomer/checkout.html', context)


@login_required
def delete_order(request, order_id):
    try:
        # Fetch the order to be deleted
        order_to_delete = Order.objects.get(id=order_id, user=request.user)

        # Delete the order
        order_to_delete.delete()

        # Optionally, you can add a success message
        messages.success(request, "Order deleted successfully.")
    except Order.DoesNotExist:
        # Handle the case where the order does not exist or does not belong to the user
        messages.error(request, "Order not found or not accessible.")

    # Redirect back to the checkout page
    return redirect('checkout')

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
            time_since_update = timezone.now() - order.updated_at

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

@login_required
def submit_order(request):
    user = request.user
    pending_orders = Order.objects.filter(user=user, status='pending')
    markup = Markup.get_instance()

    if not pending_orders.exists():
        return redirect('../home')

    if request.method == 'POST':
        for order in pending_orders:
            num_cones = len(order.cones)
            drone = find_available_drone(num_cones)
            if drone:
                order_total = order.get_order_total()
                markup_factor = Decimal(str(markup.markup_percentage * Decimal('.01')))
                order_total_without_markup = order_total - (order_total * markup_factor)
                drone.dollar_revenue += order_total_without_markup / 2
                order.drone = drone
                order.status = "delivering"
                order.updated_at = timezone.now()
                order.save()

                # Update quantities in the database
                for cone in order.cones:
                    # Subtract Ice Cream quantity
                    ice_cream = IceCream.objects.get(flavor=cone['flavor']['flavor'])
                    ice_cream.qty -= 5
                    ice_cream.save()

                    # Subtract Cone quantity
                    cone_item = Cone.objects.get(name=cone['cone']['name'])
                    cone_item.qty -= 1
                    cone_item.save()

                    # Subtract Toppings quantity
                    for topping in cone['toppings']:
                        topping_item = Topping.objects.get(name=topping['name'])
                        topping_item.qty -= 1
                        topping_item.save()

                drone.in_flight = True                
                drone.save()

                timer = threading.Timer(600, update_drone_status, args=[drone.id])
                timer.start()

                order_timer = threading.Timer(600, update_order_status, args=[order.id])
                order_timer.start()

            else:
                messages.error(request, 'No drones are available for delivery right now. Please try again later.')

            if not messages.get_messages(request):
                return redirect('../home')

    return redirect('../checkout')


def update_order_status(order_id):
    print("updating order to delivered")
    order = Order.objects.get(id=order_id)
    order.status = "delivered"
    order.save()


def update_drone_status(drone_id):
    print("updating drone to available")
    Drone.objects.filter(id=drone_id).update(in_flight=False)


def find_available_drone(num_cones):
    # Define drone size based on the number of cones
    if num_cones <= 1:
        size_options = ['small', 'medium', 'large']
    elif num_cones <= 4:
        size_options = ['medium', 'large']
    else:
        size_options = ['large']

    # Query for available drones of the appropriate size or larger
    return Drone.objects.filter(size__in=size_options, enabled=True, in_flight=False).first()



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
    
@drone_owner_required
def manageMyDrone(request):
    drones = Drone.objects.filter(owner=request.user)   
    total_minutes = 0     
    for drone in drones:
        droneOrders = Order.objects.filter(drone=drone)
        total_drone_minutes_worked = 0
        for order in droneOrders:
            total_drone_minutes_worked += 10
            total_minutes += 10
        drone.hours_worked = round(total_drone_minutes_worked / 60, 2)
    
    total_drones = drones.count()
    total_hours_worked = round((total_minutes / 60), 2) if total_drones > 0 else 0
    total_revenue = drones.aggregate(Sum('dollar_revenue'))['dollar_revenue__sum'] if total_drones > 0 else 0
    avg_hours_per_drone = round((total_hours_worked / total_drones), 2) if total_drones > 0 else 0
    avg_rev_per_drone = round((total_revenue / total_drones), 2) if total_drones > 0 else 0

    return render(request, "DroneCustomer/manageMyDrone.html", {
        'drones': drones,
        'total_revenue':total_revenue,
        'avg_hours_per_drone': avg_hours_per_drone,
        'avg_rev_per_drone': avg_rev_per_drone,
        })


@drone_owner_required
def customerCreateDrone(request):
    if request.method == 'POST':
        form = DroneForm(request.POST)
        if form.is_valid():
            drone = form.save(commit=False)
            drone.owner = request.user
            drone.minutes_worked = 0.0
            drone.dollar_revenue = 0.00
            drone.save()
            return redirect('manage_my_drone')
    else:
        form = DroneForm()
    return render(request, 'DroneCustomer/customer_create_drone.html', {'form': form, 'action_title': 'Add'})


@drone_owner_required
def customerEditDrone(request, drone_id):
    drone = get_object_or_404(Drone, pk=drone_id, owner=request.user)
    if request.method == 'POST':
        form = DroneForm(request.POST, instance=drone)
        if form.is_valid():
            form.save()
            return redirect('manage_my_drone')
    else:
        form = DroneForm(instance=drone)

    return render(request, 'DroneCustomer/customer_create_drone.html', {'form': form, 'action_title': 'Edit'})


@drone_owner_required
def customerDeleteDrone(request, drone_id):
    drone = get_object_or_404(Drone, pk=drone_id, owner=request.user)
    if request.method == 'POST':
        drone.delete()
        return redirect('manage_my_drone')
    return render(request, 'DroneCustomer/customer_delete_drone.html', {'drone': drone})