from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return render(request, "DroneAdmin/index.html")


def drone_management(request):
    return render(request, "DroneAdmin/drone_management.html")


def inventory(request):
    return render(request, "DroneAdmin/inventory.html")


def sales(request):
    return render(request, "DroneAdmin/sales.html")
