from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("account/", views.account, name="account"),
    path("login/", views.login, name="login"),
    path("managedrones/", views.droneManagement, name="mydrones"),
    path("signup/", views.signUp, name="signup"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup"),
    path("signup/droneOwnerCreation.html/", views.droneOwnerCreation, name="drownownersignup")
]