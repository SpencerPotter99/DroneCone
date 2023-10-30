from django.shortcuts import render, redirect, get_object_or_404

from .forms import DroneForm, IceCreamForm, ConeForm, ToppingForm
from DroneCustomer.models import Drone, IceCream, Cone, Topping

def index(request):
    return render(request, "DroneAdmin/dashboard.html")


def drone_management(request):
    drones = Drone.objects.all()
    return render(
        request,
        "DroneAdmin/drone_management.html",
        { 'drones' : drones }
    )


def add_drone(request, drone_id=None):
    if drone_id:
        drone = get_object_or_404(Drone, pk = drone_id)
    else:
        drone = None

    if request.method == 'POST':
        form = DroneForm(request.POST, instance=drone)
        if form.is_valid():
            form.save()
            return redirect('drone_management')
    else:
        form = DroneForm(instance=drone)
    return render(request, 'DroneAdmin/add_drone.html', {'form': form})


def inventory(request):
    ice_creams = IceCream.objects.all()
    cones = Cone.objects.all()
    toppings = Topping.objects.all()

    return render(
        request,
        "DroneAdmin/inventory.html",
        {
            'ice_creams': ice_creams,
            'cones': cones,
            'toppings': toppings
        }
    )


def add_ice_cream(request, item_id=None):
    if item_id:
        ice_cream = get_object_or_404(IceCream, pk=item_id)
    else:
        ice_cream = None

    if request.method == 'POST':
        form = IceCreamForm(request.POST, instance=ice_cream)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = IceCreamForm(instance=ice_cream)

    return render(request, 'DroneAdmin/add_ice_cream.html', {'form': form})


def add_cone(request, item_id=None):
    if item_id:
        cone = get_object_or_404(Cone, pk=item_id)
    else:
        cone = None

    if request.method == 'POST':
        form = ConeForm(request.POST, instance=cone)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ConeForm(instance=cone)

    return render(request, 'DroneAdmin/add_cone.html', {'form': form})


def add_topping(request, item_id=None):
    if item_id:
        topping = get_object_or_404(Topping, pk=item_id)
    else:
        topping = None

    if request.method == 'POST':
        form = ToppingForm(request.POST, instance=topping)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ToppingForm(instance=topping)

    return render(request, 'DroneAdmin/add_topping.html', {'form': form})


def sales(request):
    return render(request, "DroneAdmin/sales.html")
