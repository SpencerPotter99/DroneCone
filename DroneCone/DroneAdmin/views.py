from django.shortcuts import render, redirect, get_object_or_404

from .forms import DroneForm
from DroneCustomer.models import Drone

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
    return render(request, "DroneAdmin/inventory.html")


def sales(request):
    return render(request, "DroneAdmin/sales.html")
