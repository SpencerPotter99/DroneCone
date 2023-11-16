from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, ModelForm, TextInput
from .models import Profile
from django import forms




class CustomUserCreationForm(UserCreationForm):
    email = EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'custom-email-input border border-gray-400 rounded'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
        widgets = {
            'username': TextInput(attrs={'class': 'custom-username-input border border-gray-400 rounded'}),
            'password1': forms.PasswordInput(attrs={'class': 'custom-password1-input border border-gray-400 rounded'}),
            'password2': forms.PasswordInput(attrs={'class': 'custom-password2-input border border-gray-400 rounded'}),
        }

        

class CustomUserForm(ModelForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone', 'drone_owner')
