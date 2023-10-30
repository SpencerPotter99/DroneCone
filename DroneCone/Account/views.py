from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from .forms import CustomUserCreationForm
from django.http import HttpResponse


def loginPage(request):
    return render(request, 'authenticate/login.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, try again...")
            return redirect('loginPage')
    else:
        return render(request, 'authenticate/login.html', {})

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # context = {'email': email, 'password':password}
            user = authenticate(username=username, password=password)
            # return render(request, 'authenticate/customerCreation.html', context)

            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect('home')
        
    else: 
        form = CustomUserCreationForm()

    return render(request, 'authenticate/customerCreation.html', {'form':form})
