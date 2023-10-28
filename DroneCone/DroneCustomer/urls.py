from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("orderhistory/", views.orderHistory, name="orderhistory"),
    path("login/", views.login, name="login"),
    path("mydrones/", views.droneManagement, name="mydrones"),
    path("signup/", views.signUp, name="signup"),
    path("droneOwnerCreation/", views.droneOwnerCreation, name="droneOwnerCreation"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup")
]