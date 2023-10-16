from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('drone_management/', views.drone_management, name="drone_management"),
    path('inventory/', views.inventory, name="inventory"),
    path('sales/', views.sales, name="sales")
]