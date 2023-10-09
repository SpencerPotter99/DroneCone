from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/", views.checkout, name="checkout"),
    path("orderhistory/", views.orderHistory, name="orderhistory"),
    path("login/", views.login, name="login"),
    path("droneManagement/", views.droneManagement, name="dronemanagement")
]