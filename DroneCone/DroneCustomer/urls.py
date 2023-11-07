from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("account/", views.account, name="account"),
    # path("login/", views.login, name="login"),
    path("managedrones/", views.droneManagement, name="mydrones"),
    path("signup/", views.signUp, name="signup"),
    path("droneOwnerCreation/", views.droneOwnerCreation, name="droneOwnerCreation"),
    path("droneownersignup/", views.droneOwnerCreation, name="droneownersignup"),
    path("editaccount/", views.editAccount, name="editaccount"),
    path("signup/droneOwnerCreation.html/", views.droneOwnerCreation, name="drownownersignup"),
    path('menu-items/', MenuItemsAPI.as_view(), name='menu-items-api'),
    path('topping-items/', ToppingsItemsAPI.as_view(), name='topping-items-api'),
    path('cone-items/', ConeItemsAPI.as_view(), name='cone-items-api'),
    path('create_orders/', OrderCreateView.as_view(), name='order-create'),
    path('create_icecreamcone/', IceCreamConeCreateView.as_view(), name='create_icecreamcone'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('order_history/', OrderListView.as_view(), name='order_history'),
    path('get_user_id/', GetUserIdView.as_view(), name='get_user_id'),
]