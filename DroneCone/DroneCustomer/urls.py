from django.urls import path

from . import views
from .views import MenuItemsAPI, OrderCreateView, ToppingsItemsAPI, ConeItemsAPI

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("account/", views.account, name="account"),
    path("login/", views.login, name="login"),
    path("managedrones/", views.droneManagement, name="mydrones"),
    path("signup/", views.signUp, name="signup"),
    path("droneOwnerCreation/", views.droneOwnerCreation, name="droneOwnerCreation"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup"),
    path("editaccount/", views.editAccount, name="editaccount"),
    path("signup/droneOwnerCreation.html/", views.droneOwnerCreation, name="drownownersignup"),
    path('menu-items/', MenuItemsAPI.as_view(), name='menu-items-api'),
    path('topping-items/', ToppingsItemsAPI.as_view(), name='topping-items-api'),
    path('cone-items/', ConeItemsAPI.as_view(), name='cone-items-api'),
    path('orders/', OrderCreateView.as_view(), name='order-create')
]