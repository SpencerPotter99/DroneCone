from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('drone_management/', views.drone_management, name="drone_management"),
    path('drone_management/add_drone/', views.add_drone, name='add_drone'),
    path('inventory/', views.inventory, name="inventory"),
    path('sales/', views.sales, name="sales")
]