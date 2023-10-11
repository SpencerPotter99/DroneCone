from django import path

from . import views

urlpatterns = [
    path('', views.drone_management, name="drone_management"),
    path('', views.inventory, name="inventory"),
    path('', views.sales, name="sales")
]