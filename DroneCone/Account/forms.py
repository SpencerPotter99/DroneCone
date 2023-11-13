from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, EmailField
from django.utils.translation import gettext_lazy as _

from .models import Profile

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserCreationForm(admin_forms.BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone', 'drone_owner')
