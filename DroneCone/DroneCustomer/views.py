from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'DroneCustomer/home.html')

def checkout(request):
    return render(request, 'DroneCustomer/checkout.html')

def orderHistory(request):
    return HttpResponse("This is the orderHistory page")

def login(request):
    return render(request, 'DroneCustomer/login.html')

def droneManagement(request):
    return render(request, 'DroneCustomer/droneManager.html')

def droneOwnerCreation(request):
    return render(request, 'DroneCustomer/droneOwnerCreation.html')

def signUp(request):
    return render(request, 'DroneCustomer/customerCreation.html')