from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Drone
from django.contrib.auth.decorators import login_required
from ..customerDecorators import drone_owner_required
from rest_framework.test import APIClient
from django.test import TestCase



class TestDroneOwnerRequiredViews(TestCase):
    def setUp(self):
        self.client = APIClient()

        ## Creating a drone Owner
        self.droneOwner_form_data = {
            'username': 'testDroneOwner',
            'password1': 'testpassword1212',
            'password2': 'testpassword1212',
            'email': 'test1@gmail.com',
            'drone_owner' : True
        }
        url = reverse('account:drone_owner_creation')
        response = self.client.post(url, self.droneOwner_form_data)

        # Check if the creation was successful (status code 302 for redirect)
        self.assertEqual(response.status_code, 302)

        self.user = User.objects.get(username=self.droneOwner_form_data['username'])
        self.assertIsNotNone(self.user)

        self.drone = None

    @login_required
    @drone_owner_required
    def test_manage_my_drone_view(self):
        response = self.client.get(reverse('manage_my_drone'))
        self.assertEqual(response.status_code, 200)

    @login_required
    @drone_owner_required
    def test_customer_create_drone_view(self):
        response = self.client.get(reverse('customer_create_drone'))
        self.assertEqual(response.status_code, 200)


    ## creates a drone with name, assigns it to self.user, assigns it to self.drone
    def createDrone(self, name):
        form_data = {
            'owner': self.user,
            'name': name,
            'size': 'small',
            'drone_weight_g': 500,
            'battery_capacity_mAh': 2000,
            'battery_voltage': 11.1,
            'battery_percentage': 80,
            'enabled': True,
        }
        response = self.client.post(reverse('customer_create_drone'), form_data)
        self.drone = Drone.objects.filter(name='testDrone')[0]


    @login_required
    @drone_owner_required
    def test_customer_create_drone_form_submission(self):
        self.createDrone("testDrone")
        self.assertTrue(Drone.objects.filter(name='testDrone').exists())
        self.drone = Drone.objects.filter(name='testDrone')


    ## creates a drone, changes its attributes, makes tests
    @login_required
    @drone_owner_required
    def test_customer_edit_drone_form_submission(self):
        self.createDrone("testDrone")
        # Update the drone with new values
        updated_data = {
            'owner': self.user,
            'name': 'updatedDrone',
            'size': 'medium',
            'drone_weight_g': 700,
            'battery_capacity_mAh': 3000,
            'battery_voltage': 12.0,
            'battery_percentage': 90,
            'enabled': False,
        }

        response = self.client.post(reverse('customer_edit_drone', args=[self.drone.id]), updated_data)
        self.assertEqual(response.status_code, 302)

        # Refresh the drone instance from the database
        updated_drone = Drone.objects.get(id=self.drone.id)

        # Check if the drone has been updated with the new values
        self.assertEqual(updated_drone.name, 'updatedDrone')
        self.assertEqual(updated_drone.size, 'medium')
        self.assertEqual(updated_drone.drone_weight_g, 700)
        self.assertEqual(updated_drone.battery_capacity_mAh, 3000)
        self.assertEqual(updated_drone.battery_voltage, 12.0)
        self.assertFalse(updated_drone.enabled)

    ## creates drone, deletes it
    @login_required
    @drone_owner_required
    def test_customer_delete_drone_form_submission(self):
        self.createDrone("testDrone")
        response = self.client.post(reverse('customer_delete_drone', args=[self.drone.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Drone.objects.filter(name='testDrone').exists())

# class AccountandOrders(TestCase):
#     def setUp(self):
#         ## Creating a regular user
#         self.client = APIClient()
#         self.user_form_data = {
#             'username': 'testUser',
#             'password1': 'testpassword1212',
#             'password2': 'testpassword1212',
#             'email': 'test83@gmail.com',
#             'drone_owner' : True
#         }
#         response = self.client.post(reverse('account:signup'), self.user_form_data)
#         self.client.login(username='testUser', password='testpassword1212')


#         # Check if the creation was successful (status code 302 for redirect)
#         self.assertEqual(response.status_code, 302)

#         self.user = User.objects.get(username=self.user_form_data['username'])
#         self.assertEqual(self.user.email, 'test83@gmail.com')
#         self.assertIsNotNone(self.user)
        

#     def test_update_account_success(self):
#         # Simulate a POST request with valid data

#         response = self.client.post(reverse('update_account'), {
#             'email': 'newemail@example.com',
#             'address': 'New Address',
#             'phone': '1234567890',
#             'current_password': 'testpassword',
#             'new_password': 'newpassword123',
#             'confirm_password': 'newpassword123',
#             'drone_owner': True,
#         })

#         # Check if the response redirects to the account page
#         self.assertRedirects(response, reverse('editaccount'))

#         # Refresh the user from the database to get the updated information
#         self.user.refresh_from_db()

#         # Check if the user's information has been updated
#         self.assertEqual(self.user.email, 'newemail@example.com')
#         self.assertEqual(self.user.profile.address, 'New Address')
#         self.assertEqual(self.user.profile.phone, '1234567890')
#         self.assertTrue(self.user.profile.drone_owner)

#         # Check if the password has been updated
#         self.assertTrue(self.user.check_password('newpassword123'))

class UpdateAccountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

    def test_update_account_success(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Define the update data
        update_data = {
            'email': 'newemail@example.com',
            'address': 'New Address',
            'phone': '1234567890',
            'current_password': 'testpassword',
            'new_password': 'newpassword',
            'confirm_password': 'newpassword',
            'drone_owner': 'on',
        }

        # Make a POST request to update the account
        response = self.client.post(reverse('update_account'), update_data)

        # Check if the response is a redirect to the account page
        self.assertRedirects(response, reverse('account'))

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Check if the user data is updated
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.profile.address, 'New Address')
        self.assertEqual(self.user.profile.phone, '1234567890')
        self.assertTrue(self.user.profile.drone_owner)
        
        # Check if the password is updated
        self.assertTrue(self.user.check_password('newpassword'))

    