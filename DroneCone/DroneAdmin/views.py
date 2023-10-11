from django.shortcuts import render

def drone_management(request):
    return render(request, "DroneAdmin.drone_management.html")

def inventory(request):
    return render(request, "DroneAdmin.inventory.html")


def sales(request):
    return render(request, "DroneAdmin.sales.html")
