from django.shortcuts import render

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


def inventory(request):
    return render(request, "DroneAdmin/inventory.html")


def sales(request):
    return render(request, "DroneAdmin/sales.html")
