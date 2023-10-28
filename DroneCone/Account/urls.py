from django.urls import path
from . import views

from . import views

urlpatterns = [
    path("customerLogin/", views.login_user, name='login'),
]