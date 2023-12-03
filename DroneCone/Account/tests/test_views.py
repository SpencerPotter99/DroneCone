from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from ..forms import CustomUserCreationForm, ProfileForm
from rest_framework.test import APIClient


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = None

    def test_register_view(self):
        user_data = {
            'username': 'testuser',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test@gmail.com',
            'drone_owner' : True
        }

        url = reverse('account:signup')
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 302)
        self.user = User.objects.get(username=user_data['username'])
        self.assertIsNotNone(self.user)

         # user created as expected, user logged in, redirects to home
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def tryCreatingAccount(self, username, password1, password2, email, droneOwner):
        invalid_data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'drone_owner' : droneOwner
            }
        url = reverse('account:signup')
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, 200)
        try:
            user = User.objects.get(username=invalid_data['username'])
            self.fail("User should not have been created")
        except User.DoesNotExist:
        # User does not exist, which is expected
            pass


    def createValidUser(self, username, password1, password2, email, droneOwner):
        valid_data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'drone_owner' : droneOwner
            }
        url = reverse('account:signup')
        response = self.client.post(url, valid_data)
        self.assertEqual(response.status_code, 302)
        

    def test_invalid_register_view(self):
        # Test with unequal passwords
        self.tryCreatingAccount('testAnotherUser', 'testpassword1212', 'wrongConfirmation', 'test@gmail.com', False)

        # Short passwords
        self.tryCreatingAccount('user1', 'short', 'short', 'test@gmail.com', False)

        #Test no @ symbol in email
        self.tryCreatingAccount('validUsername', 'validpassword123123', 'validpassword123123', 'noatsymbol', False)


    def test_drone_owner_register_view(self):
        # Create Drone Owner
        droneOwner_data = {
            'username': 'testdroneOwner',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test@gmail.com',
            'drone_owner' : True
        }
        url = reverse('account:drone_owner_creation')
        response = self.client.post(url, droneOwner_data)
        self.assertEqual(response.status_code, 302)

        # User and profile were created as expected
        user = User.objects.get(username=droneOwner_data['username'])
        self.assertIsNotNone(user)
        
         # Check that the user is logged in after registration
        self.assertTrue(user.is_authenticated)

        # Check that the user is redirected to the 'home' page
        self.assertRedirects(response, reverse('manage_my_drone'))

    def test_logout_view(self):
        self.createValidUser("testAnotherUser", 'passwordduh123', 'passwordduh123', 'test@gmail.com', False)
        self.user = User.objects.get(username='testAnotherUser')
        self.assertIsNotNone(self.user)
        self.assertTrue(self.user.is_authenticated)

        # Test POST request to log out
        response_post = self.client.post(reverse('account:logout'))

        # Check that the response is a redirect (302 Found)
        self.assertEqual(response_post.status_code, 302)

        # Check that the user is not authenticated after logout
        # self.assertFalse(self.user.is_authenticated)

        # Check that the user is redirected to the expected URL (in this case, home)
        self.assertRedirects(response_post, reverse('account:login'))
        