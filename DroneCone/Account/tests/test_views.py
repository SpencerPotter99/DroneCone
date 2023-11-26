from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from forms import CustomUserCreationForm, ProfileForm
from views import (
    RegisterView,
    DroneOwnerRegisterView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    ProfileView,
)

class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test@gmail.com',
            'drone_owner' : False
        }
        self.droneOwner_user_data = {
            'username': 'testDroneOwner',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test@gmail.com',
            'drone_owner' : True
        }
        
        self.user = User.objects.create_user(**self.user_data)


    def test_register_view(self):
        url = reverse('signup')
        request = self.factory.post(url, data=self.user_data)
        response = RegisterView(request)
        self.assertEqual(response.status_code, 302)

         # user created as expected, user logged in, redirects to home
        user = User.objects.get(username=self.user_data['username'])
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

        # Test with unequal passwords
        invalid_data = {
            'username': 'testAnotherUser',
            'password1': 'testpassword1212',
            'password2': 'wrongpassword',
            'email': 'test@gmail.com',
            'drone_owner' : False
            }
        request = self.factory.post(url, data=invalid_data)
        response = RegisterView(request)

        # Test with used Username
        invalid_data = {
            'username': 'testuser',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test@gmail.com',
            'drone_owner': False
            }
        request = self.factory.post(url, data=invalid_data)
        response = RegisterView(request)


    def test_drone_owner_register_view(self):
        url = reverse('drone_owner_creation')
        request = self.factory.post(url, data=self.droneOwner_user_data)
        response = DroneOwnerRegisterView(request)
        self.assertEqual(response.status_code, 302)

        # User and profile were created as expected
        user = User.objects.get(username=self.droneOwner_user_data['username'])
        self.assertIsNotNone(user)
        
         # Check that the user is logged in after registration
        self.assertTrue(user.is_authenticated)

        # Check that the user is redirected to the 'home' page
        self.assertRedirects(response, reverse('manage_my_drone'))

        # Test with unequal passwords
        invalid_data = {
            'username': 'testAnotherUser',
            'password1': 'testpassword1212',
            'password2': 'wrongpassword',
            'email': 'test@gmail.com',
            'drone_owner' : True
            }
        request = self.factory.post(url, data=invalid_data)
        response = RegisterView(request)

        # Test with used Username
        invalid_data = {
            'username': 'testuser',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test@gmail.com',
            'drone_owner' : True
            }
        request = self.factory.post(url, data=invalid_data)
        response = RegisterView(request)


    def test_login_view(self):
        url = reverse('login')
        request = self.factory.get(url)
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)  # Expect a successful GET request

        # Test with valid credentials
        valid_credentials = {
            'username': 'testuser',
            'password': 'testpassword1212',
        }
        request = self.factory.post(url, data=valid_credentials)
        response = LoginView.as_view()(request)

        # Check that the response is a redirect (successful login)
        self.assertEqual(response.status_code, 302)

        # Check that the user is logged in after login
        currUser = User.objects.get(username='testuser')
        self.assertTrue(currUser.is_authenticated)

        # Check that the user is redirected to the correct page
        if not currUser.drone_owner:
            self.assertRedirects(response, reverse('home'))
        elif currUser.drone_owner:
            self.assertRedirects(response, reverse('manage_my_drone'))
        

        # Check with invalid credentials
        invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpassword'
            }
        request = self.factory.post(url, data=invalid_credentials)
        response = LoginView.as_view()(request)

        # Check that the response is not a redirect (login failed)
        self.assertEqual(response.status_code, 200)

        # Check that the form errors are present in the response
        self.assertContains(response, 'Please enter a correct password.')

        # Check when the user is already authenticated
        authenticated_user = User.objects.create_user(username='authenticated_user', password='testpassword')
        request = self.factory.post(url, data=valid_credentials)
        request.user = authenticated_user
        response = LoginView.as_view()(request)

        # Check that the response is a redirect (user is already authenticated)
        self.assertEqual(response.status_code, 302)

        # Check that the user is redirected to the 'home' page
        self.assertRedirects(response, reverse('home'))

        # Check that a message is set in the session indicating the user is already authenticated
        self.assertIn('You are already logged in.', request.session.get('messages').data[0].message)

    def test_profile_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword1212')

        # Test the ProfileView
        url = reverse('profile')

        # Test with valid form data
        valid_form_data = {
            'username': 'new_username',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'profile-bio': 'A short bio about John Doe.',
        }

        request = self.factory.post(url, data=valid_form_data)
        response = ProfileView.as_view()(request)

        # Check that the response is a redirect (successful form submission)
        self.assertEqual(response.status_code, 302)

        # Check that the user profile is updated as expected
        updated_user = User.objects.get(username='new_username')
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.email, 'john.doe@example.com')
        self.assertEqual(updated_user.profile.bio, 'A short bio about John Doe.')

        # Check that a success message is set in the session
        self.assertIn('Your profile is updated successfully', request.session.get('messages').data[0].message)

        # Test with invalid form data
        invalid_form_data = {
            'username': '',  # Invalid username
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid_email',  # Invalid email
            'profile-bio': 'A short bio about John Doe.',
        }

        request = self.factory.post(url, data=invalid_form_data)
        response = ProfileView.as_view()(request)

        # Check that the response is not a redirect (form submission failed)
        self.assertEqual(response.status_code, 200)

        # Check that the form errors are present in the response
        self.assertContains(response, 'This field is required.')
        self.assertContains(response, 'Enter a valid email address.')

        # Check that the user profile is not updated with invalid data
        self.assertNotEqual(updated_user.username, '')
        self.assertNotEqual(updated_user.email, 'invalid_email')

        # You can add more assertions based on the expected behavior of your view