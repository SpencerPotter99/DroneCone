from django.urls import path

from .views import *
from . import views

app_name = "account"
urlpatterns = [
    path("signup/", views.RegisterView, name='signup'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),

    path("change-password/", PasswordChangeView.as_view(), name='password_change'),
    path("change-password/done/", PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path("profile/", view=ProfileView.as_view(), name="profile"),

    path('drone-owner-creation/', views.DroneOwnerRegisterView, name='drone_owner_creation')

]
