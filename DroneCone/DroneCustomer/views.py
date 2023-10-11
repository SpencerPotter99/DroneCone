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
    return HttpResponse("This is the login page")

def droneManagment(request):
    return HttpResponse("This is the Drone Management page")