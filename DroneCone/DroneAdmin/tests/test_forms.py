from django.test import TestCase
from DroneAdmin.forms import UserForm, ProfileForm, DroneForm, IceCreamForm, ToppingForm, ConeForm
from django.contrib.auth.models import User

class UserFormTest(TestCase):

    def test_user_form_valid_data(self):
        form_data = {'username': 'testuser', 'email': 'testuser@example.com', 'is_staff': True}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_data(self):
        form_data = {'username': '', 'email': 'invalid_email', 'is_staff': 'invalid'}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())