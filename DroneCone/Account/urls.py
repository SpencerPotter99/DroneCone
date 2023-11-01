from django.urls import path
from . import views

from . import views

urlpatterns = [
    path("customerLogin/", views.loginPage, name='loginPage'),
    path("loginFunction/", views.login_user, name='login'),
    path("createAccount/", views.register_user, name='createAccountPage'),

]