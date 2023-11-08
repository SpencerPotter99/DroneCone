from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("account/", views.account, name="account"),
    path("signup/", views.signUp, name="signup"),
    path("edit_account/", views.editAccount, name="editaccount"),
    path('update-account/', views.update_account, name='update_account'),
    path('create_icecreamcone/', IceCreamConeCreateView.as_view(), name='create_icecreamcone'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('order_history/', OrderListView.as_view(), name='order_history'),
    path('get_user_id/', GetUserIdView.as_view(), name='get_user_id'),
    path("manage-drones/", views.droneManagement, name="my_drones"),
    # Remove ?
    path("drone-owner-creation/", views.droneOwnerCreation, name="drone_owner_creation"),
    path("drone-owner-signup/", views.droneOwnerCreation, name="drone_owner_signup"),
    #
    path("edit-account/", views.editAccount, name="edit_account"),
    path('menu-items/', MenuItemsAPI.as_view(), name='menu_items_api'),
    path('topping-items/', ToppingsItemsAPI.as_view(), name='topping_items_api'),
    path('cone-items/', ConeItemsAPI.as_view(), name='cone_items_api'),
    path('orders/', OrderCreateView.as_view(), name='order_create')
]