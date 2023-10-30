from django.shortcuts import render
from .models import Order
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'DroneCustomer/index.html')

def home(request):
    return render(request, 'DroneCustomer/home.html')

def checkout(request):
    return render(request, 'DroneCustomer/checkout.html')



def account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'DroneCustomer/account.html', context)

def login(request):
    return render(request, 'DroneCustomer/login.html')

def droneManagement(request):
    return render(request, 'DroneCustomer/droneManager.html')

def droneOwnerCreation(request):
    return render(request, 'DroneCustomer/droneOwnerCreation.html')

def signUp(request):
    return render(request, 'DroneCustomer/customerCreation.html')

def editAccount(request):
    return render(request, 'DroneCustomer/editAccount.html')
