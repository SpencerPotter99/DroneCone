from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, ModelForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class CustomUserForm(ModelForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone', 'drone_owner')
