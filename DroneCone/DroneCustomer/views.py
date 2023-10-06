from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'DroneCustomer/home.html')

def checkout(request):
    return HttpResponse("This is the Checkout page")

def orderHistory(request):
    return HttpResponse("This is the orderHistory page")

def login(request):
    return HttpResponse("This is the login page")

def droneManagment(request):
    return HttpResponse("This is the Drone Management page")