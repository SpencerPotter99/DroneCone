from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Order, Drone  # Import other models as needed
from django.contrib.auth.models import User
from decimal import Decimal
from ..models import Drone, IceCream, Topping, Cone, IceCreamCone, Order, Cart

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

def create_mock_ice_cream_empty(flavor='Chocolote', price=3.00, qty=0):
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


class HomeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.drone = Drone.objects.create(owner=self.user, name='Test Drone', drone_weight_g=100,
                                          battery_capacity_mAh=2000, battery_voltage=11.1, battery_level=1.0)

        self.ice_cream = IceCream.objects.create(flavor='Vanilla', price=Decimal('2.00'), qty=10)

        self.topping = Topping.objects.create(name='Sprinkles', price=Decimal('0.50'), qty=5)
    
        self.cone = Cone.objects.create(name='Waffle Cone', price=Decimal('1.00'), qty=20)

        self.ice_cream_cone = create_mock_ice_cream_cone(flavor=self.ice_cream,
                                                         toppings=[self.topping],
                                                         cone=self.cone,
                                                         size='small')
        self.order = create_mock_order(user=self.user, drone=self.drone, cones=[self.ice_cream_cone], status="pending")
    
    def test_home_user_not_signed_in(self):
        # Ensure the user is not logged in

        # Access the home view
        response = self.client.get(reverse('home'))

        # Check if the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if the context is not None before checking for 'user'
        if response.context is not None:
            self.assertNotIn('user', response.context)
    
    def test_home_user_signed_in(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the home view
        response = self.client.get(reverse('home'))

        # Check if the user is authenticated and the status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_home_page_successfully_loaded(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertIn('Welcome To Drone Cones', response.content.decode('utf-8'))

class HomeApiTests(TestCase):
    def setUp(self):
        # Create a test user and test objects
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.topping = Topping.objects.create(name='Sprinkles', price=Decimal('0.50'), qty=5)
        self.ice_cream = IceCream.objects.create(flavor='Vanilla', price=Decimal('2.00'), qty=10)
        self.cone = Cone.objects.create(name='Waffle Cone', price=Decimal('1.00'), qty=20)

    def test_menu_items_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the menu items view
        response = self.client.get(reverse('menu_items_api'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        expected_flavor = {'id': 1, 'flavor': 'Vanilla', 'price': '2.00', 'qty': 10}
        self.assertIn(expected_flavor, response.data)

    def test_topping_items_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the topping items view
        response = self.client.get(reverse('topping_items_api'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        expected_topping = {'id': 1, 'name': 'Sprinkles', 'price': '0.50', 'qty': 5}
        self.assertIn(expected_topping, response.data)


    def test_cone_items_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the cone items view
        response = self.client.get(reverse('cone_items_api'))

        expected_cone = {'id': 1, 'name': 'Waffle Cone', 'price': '1.00', 'qty': 20}
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_cone, response.data)

class ConeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Cone.objects.create(name='Regular Cone', price=2.50, qty=10)

    def test_name_label(self):
        cone = Cone.objects.get(id=1)
        field_label = cone._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_price_label(self):
        cone = Cone.objects.get(id=1)
        field_label = cone._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

    def test_qty_label(self):
        cone = Cone.objects.get(id=1)
        field_label = cone._meta.get_field('qty').verbose_name
        self.assertEqual(field_label, 'qty')

    def test_name_max_length(self):
        cone = Cone.objects.get(id=1)
        max_length = cone._meta.get_field('name').max_length
        self.assertEqual(max_length, 127)

    def test_price_default_value(self):
        cone = Cone.objects.get(id=1)
        default_value = cone._meta.get_field('price').default
        self.assertEqual(default_value, 0)

    def test_qty_default_value(self):
        cone = Cone.objects.get(id=1)
        default_value = cone._meta.get_field('qty').default
        self.assertEqual(default_value, 0)

    def test_object_name(self):
        cone = Cone.objects.get(id=1)
        expected_object_name = f"{cone.name}"
        self.assertEqual(expected_object_name, str(cone))

class IceCreamModelTest(TestCase):

    def setUp(self):
        IceCream.objects.create(flavor='Vanilla', price=1.50, qty=10)
        IceCream.objects.create(flavor='Chocolate', price=2.00, qty=15)

    def test_ice_cream_flavor(self):
        vanilla = IceCream.objects.get(flavor='Vanilla')
        chocolate = IceCream.objects.get(flavor='Chocolate')
        self.assertEqual(str(vanilla), 'Vanilla')
        self.assertEqual(str(chocolate), 'Chocolate')

    def test_ice_cream_price(self):
        vanilla = IceCream.objects.get(flavor='Vanilla')
        chocolate = IceCream.objects.get(flavor='Chocolate')
        self.assertEqual(vanilla.price, 1.50)
        self.assertEqual(chocolate.price, 2.00)

    def test_ice_cream_qty(self):
        vanilla = IceCream.objects.get(flavor='Vanilla')
        chocolate = IceCream.objects.get(flavor='Chocolate')
        self.assertEqual(vanilla.qty, 10)
        self.assertEqual(chocolate.qty, 15)

class ToppingModelTest(TestCase):

    def setUp(self):
        Topping.objects.create(name='Chocolate Sprinkles', price=0.50, qty=20)
        Topping.objects.create(name='Caramel Sauce', price=0.75, qty=15)

    def test_topping_name(self):
        topping1 = Topping.objects.get(id=1)
        topping2 = Topping.objects.get(id=2)
        self.assertEqual(str(topping1), 'Chocolate Sprinkles')
        self.assertEqual(str(topping2), 'Caramel Sauce')

    def test_topping_price(self):
        topping1 = Topping.objects.get(id=1)
        topping2 = Topping.objects.get(id=2)
        self.assertEqual(topping1.price, 0.50)
        self.assertEqual(topping2.price, 0.75)

    def test_topping_qty(self):
        topping1 = Topping.objects.get(id=1)
        topping2 = Topping.objects.get(id=2)
        self.assertEqual(topping1.qty, 20)
        self.assertEqual(topping2.qty, 15)

class IceCreamConeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ice_cream = IceCream.objects.create(flavor='Vanilla', price=1.50)
        cone = Cone.objects.create(name='Regular Cone', price=2.00, qty=10)
        topping = Topping.objects.create(name='Sprinkles', price=0.50)

        # Create an instance of IceCreamCone
        ice_cream_cone = IceCreamCone.objects.create(size='small', flavor=ice_cream, cone=cone)

        # Use the set method on the toppings instance
        ice_cream_cone.toppings.set([topping])

    def test_object_name(self):
        ice_cream_cone = IceCreamCone.objects.get(pk=1)  # Adjust the primary key accordingly
        expected_object_name = "Vanilla | Regular Cone | small | ['Sprinkles']"
        actual_object_name = str(ice_cream_cone)
        self.assertIn(expected_object_name, actual_object_name)

    def test_size_choices(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        size_choices = ice_cream_cone._meta.get_field('size').choices
        self.assertEqual(size_choices, IceCreamCone.SIZE_CHOICES)

    def test_flavor_label(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        field_label = ice_cream_cone._meta.get_field('flavor').verbose_name
        self.assertEqual(field_label, 'flavor')

    def test_toppings_label(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        field_label = ice_cream_cone._meta.get_field('toppings').verbose_name
        self.assertEqual(field_label, 'toppings')

    def test_cone_label(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        field_label = ice_cream_cone._meta.get_field('cone').verbose_name
        self.assertEqual(field_label, 'cone')

    def test_size_max_length(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        max_length = ice_cream_cone._meta.get_field('size').max_length
        self.assertEqual(max_length, 10)

    def test_get_cone_info(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        expected_cone_info = {
            'size': 'small',
            'flavor': 'Vanilla',
            'toppings': ['Sprinkles'],
            'cone': 'Regular Cone',
            'price': '4.00'
        }
        self.assertEqual(ice_cream_cone.get_cone_info(), expected_cone_info)

    def test_get_price(self):
        ice_cream_cone = IceCreamCone.objects.get(id=1)
        expected_price = 4.00
        self.assertEqual(ice_cream_cone.get_price(), expected_price)

class OrderModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create an order with a single cone
        self.order_data_single_cone = {
            'user': self.user,
            'cones': {'flavor': 'Vanilla', 'price': '2.50'},
            'status': 'Pending',
        }
        self.order_single_cone = Order.objects.create(**self.order_data_single_cone)

        # Create an order with multiple cones
        self.order_data_multiple_cones = {
            'user': self.user,
            'cones': [
                {'flavor': 'Chocolate', 'price': '3.00'},
                {'flavor': 'Strawberry', 'price': '2.75'},
            ],
            'status': 'Preparing',
        }
        self.order_multiple_cones = Order.objects.create(**self.order_data_multiple_cones)

    def test_order_str(self):
        self.assertEqual(str(self.order_single_cone), f"Order #{self.order_single_cone.pk} - Pending")
        self.assertEqual(str(self.order_multiple_cones), f"Order #{self.order_multiple_cones.pk} - Preparing")

    def test_get_order_total(self):
        total_single_cone = self.order_single_cone.get_order_total()
        total_multiple_cones = self.order_multiple_cones.get_order_total()

        self.assertEqual(total_single_cone, 2.50)
        self.assertEqual(total_multiple_cones, 5.75)

    def test_get_cone_info(self):
        cone_info_single = self.order_single_cone.get_cone_info()
        cone_info_multiple = self.order_multiple_cones.get_cone_info()

        self.assertEqual(cone_info_single, [{'flavor': 'Vanilla', 'price': '2.50'}])
        self.assertEqual(cone_info_multiple, [
            {'flavor': 'Chocolate', 'price': '3.00'},
            {'flavor': 'Strawberry', 'price': '2.75'},
        ])
class DroneModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a drone for testing
        self.drone_data = {
            'owner': self.user,
            'name': 'Test Drone',
            'size': 'medium',
            'drone_weight_g': 1000,
            'battery_capacity_mAh': 5000,
            'battery_voltage': Decimal('11.1'),
            'battery_level': Decimal('0.8'),
            'hours_worked': Decimal('2.5'),
            'dollar_revenue': Decimal('50.00'),
            'enabled': True,
            'in_flight': False,
        }
        self.drone = Drone.objects.create(**self.drone_data)

    def test_is_available(self):
        # Drone is enabled and not in flight, so it should be available
        self.assertTrue(self.drone.is_available())

        # Disable the drone and check availability
        self.drone.enabled = False
        self.drone.save()
        self.assertFalse(self.drone.is_available())

        # Enable the drone but set it to in flight, it should not be available
        self.drone.enabled = True
        self.drone.in_flight = True
        self.drone.save()
        self.assertFalse(self.drone.is_available())

    def test_get_drone_status(self):
        # Drone is enabled but not in flight, so the status should be "Available"
        self.assertEqual(self.drone.get_drone_status(), "Available")

        # Set the drone to in flight, the status should be "In Flight"
        self.drone.in_flight = True
        self.drone.save()
        self.assertEqual(self.drone.get_drone_status(), "In Flight")

        # Disable the drone, the status should be "Disabled"
        self.drone.enabled = False
        self.drone.save()
        self.assertEqual(self.drone.get_drone_status(), "Disabled")

    def test_drone_str(self):
        # Check the string representation of the drone
        expected_str = f"Test Drone"
        self.assertEqual(str(self.drone), expected_str)