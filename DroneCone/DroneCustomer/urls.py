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
<<<<<<< HEAD
    path("droneOwnerCreation/", views.droneOwnerCreation, name="droneOwnerCreation"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup")
=======
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup"),
    path("editaccount/", views.editAccount, name="editaccount"),
    path("signup/droneOwnerCreation.html/", views.droneOwnerCreation, name="drownownersignup")
>>>>>>> a8c06584e8f188f849d816f016afdf4abe146d33
]