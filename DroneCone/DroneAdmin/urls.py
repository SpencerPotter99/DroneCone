from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='order_history'),
    path('drone_management/', views.drone_management, name="drone_management"),
    path('drone_management/add_drone/', views.add_drone, name='add_drone'),
    path('drone_management/add_drone/<int:item_id>/', views.add_drone, name='add_drone'),
    path('drone_management/delete_drone/<int:item_id>/', views.delete_drone, name='delete_drone'),
    path('inventory/', views.inventory, name="inventory"),
    path('inventory/add_icecream/', views.add_ice_cream, name='add_ice_cream'),
    path('inventory/add_ice_cream/<int:item_id>/', views.add_ice_cream, name='add_ice_cream'),
    path('inventory/delete_ice_cream/<int:item_id>/', views.delete_ice_cream, name='delete_ice_cream'),
    path('inventory/add_cone/', views.add_cone, name='add_cone'),
    path('inventory/add_cone/<int:item_id>/', views.add_cone, name='add_cone'),
    path('inventory/delete_cone/<int:item_id>/', views.delete_cone, name='delete_cone'),
    path('inventory/add_topping/', views.add_topping, name='add_topping'),
    path('inventory/add_topping/<int:item_id>/', views.add_topping, name='add_topping'),
    path('inventory/delete_topping/<int:item_id>/', views.delete_topping, name='delete_topping'),
    path('sales/', views.sales, name="sales"),
    path('sales/edit_markup/', views.edit_markup, name='edit_markup'),
    path('user_management/', views.user_management, name='user_management'),
    path('user_management/edit_user/<int:user_id>/', views.edit_user, name="edit_user"),
    path('user_management/delete_user/<int:user_id>/', views.delete_user, name="delete_user")
]