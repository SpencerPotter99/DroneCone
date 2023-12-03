from django.test import TestCase
from DroneCustomer.models import Drone, IceCream, Topping, Cone, IceCreamCone, Order, Cart
from django.contrib.auth.models import User

class DroneModelTest(TestCase):

    def test_drone_is_available(self):
        user = User.objects.create(username='testuser')
        drone = Drone.objects.create(owner=user, name='Test Drone', drone_weight_g=100,
                                     battery_capacity_mAh=2000, battery_voltage=3.7, battery_level=0.5,
                                     enabled=True, in_flight=False)
        self.assertTrue(drone.is_available())

    # def test_drone_status_disabled(self):
        # drone = Drone.objects.create(name='Disabled Drone', enabled=False, in_flight=False)
        # self.assertEqual(drone.get_drone_status(), 'Disabled')