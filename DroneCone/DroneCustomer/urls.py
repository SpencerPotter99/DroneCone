from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/", views.checkout, name="checkout"),
    path("orderhistory/", views.orderHistory, name="orderhistory"),
    path("login/", views.login, name="login"),
    path("dronemanagement/", views.droneManagement, name="dronemanagement"),
    path("signup/", views.signUp, name="signup"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup")
]