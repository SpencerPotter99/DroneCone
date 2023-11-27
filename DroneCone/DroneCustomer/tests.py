from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, Drone  # Import other models as needed
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Drone, IceCream, Topping, Cone, IceCreamCone, Order, Cart

def create_mock_user(username='testuser', password='testpassword'):
    return User.objects.create_user(username=username, password=password)

def create_mock_drone(owner, name='Test Drone', drone_weight_g=1000, battery_capacity_mAh=5000,
                      battery_voltage=11.1, battery_level=1.0, hours_worked=0.0, dollar_revenue=0.0,
                      enabled=True, in_flight=False):
    return Drone.objects.create(owner=owner, name=name, drone_weight_g=drone_weight_g,
                                battery_capacity_mAh=battery_capacity_mAh, battery_voltage=battery_voltage,
                                battery_level=battery_level, hours_worked=hours_worked,
                                dollar_revenue=dollar_revenue, enabled=enabled, in_flight=in_flight)

def create_mock_ice_cream(flavor='Vanilla', price=3.00, qty=10):
    return IceCream.objects.create(flavor=flavor, price=price, qty=qty)

def create_mock_topping(name='Sprinkles', price=0.50, qty=5):
    return Topping.objects.create(name=name, price=price, qty=qty)

def create_mock_cone(name='Waffle Cone', price=1.00, qty=8):
    return Cone.objects.create(name=name, price=price, qty=qty)

def create_mock_ice_cream_cone(flavor, toppings, cone, size):
    ice_cream_cone = IceCreamCone.objects.create(flavor=flavor, cone=cone, size=size)
    ice_cream_cone.toppings.set(toppings)
    return ice_cream_cone

def create_mock_order(user, drone, cones, status):
    # Convert IceCreamCone objects to a serializable format
    serialized_cones = []
    for cone in cones:
        serialized_cones.append({
            'size': cone.size,
            'flavor': cone.flavor.flavor,
            'toppings': [topping.name for topping in cone.toppings.all()],
            'cone': cone.cone.name,
            'price': str(cone.get_price())
        })

    return Order.objects.create(user=user, drone=drone, cones=serialized_cones, status=status)

def create_mock_cart(user, cones=None):
    if cones is None:
        cones = []

    cart = Cart.objects.create(user=user)
    cart.cones.set(cones)
    return cart


class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.drone = Drone.objects.create(owner=self.user, name='Test Drone', drone_weight_g=100,
                                          battery_capacity_mAh=2000, battery_voltage=11.1, battery_level=1.0)

        # Create IceCream with Decimal price
        self.ice_cream = IceCream.objects.create(flavor='Vanilla', price=Decimal('2.00'), qty=10)

        # Create Topping with Decimal price
        self.topping = Topping.objects.create(name='Sprinkles', price=Decimal('0.50'), qty=5)

        # Create Cone with Decimal price
        self.cone = Cone.objects.create(name='Waffle Cone', price=Decimal('1.00'), qty=20)

        self.ice_cream_cone = create_mock_ice_cream_cone(flavor=self.ice_cream,
                                                         toppings=[self.topping],
                                                         cone=self.cone,
                                                         size='small')
        self.order = create_mock_order(user=self.user, drone=self.drone, cones=[self.ice_cream_cone], status="pending")
    
    def test_user_not_signed_in(self):
        # Ensure the user is not logged in

        # Access the home view
        response = self.client.get(reverse('home'))

        # Check if the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if the context is not None before checking for 'user'
        if response.context is not None:
            self.assertNotIn('user', response.context)
    
    def test_user_signed_in(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the home view
        response = self.client.get(reverse('home'))

        # Check if the user is authenticated and the status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
