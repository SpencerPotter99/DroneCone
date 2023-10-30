from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('drone_management/', views.drone_management, name="drone_management"),
    path('drone_management/add_drone/', views.add_drone, name='add_drone'),
    path('inventory/', views.inventory, name="inventory"),
    path('inventory/add_icecream/', views.add_ice_cream, name='add_ice_cream'),
    path('inventory/add_ice_cream/<int:item_id>/', views.add_ice_cream, name='add_ice_cream'),
    path('inventory/add_cone/', views.add_cone, name='add_cone'),
    path('inventory/add_cone/<int:item_id>/', views.add_cone, name='add_cone'),
    path('inventory/add_topping/', views.add_topping, name='add_topping'),
    path('inventory/add_topping/<int:item_id>/', views.add_topping, name='add_topping'),
    path('sales/', views.sales, name="sales")
]