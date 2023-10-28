from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class DroneOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='drone_owner')
    drones = models.ManyToManyField("Drone", related_name="owner")

    def __str__(self):
        return self.user.get_full_name()


class Drone(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='small')

    drone_weight_g = models.PositiveIntegerField()
    battery_capacity_mAh = models.PositiveIntegerField()
    battery_voltage = models.DecimalField(max_digits=5, decimal_places=2)
    battery_level = models.DecimalField(max_digits=2, decimal_places=1)  # 1.0 - 0.0

    enabled = models.BooleanField(default=True)
    in_flight = models.BooleanField(default=False)

    def available(self):
        return self.enabled and not self.in_flight

    def get_drone_status(self):
        if self.enabled:
            return "Available" if not self.in_flight else "In Flight"
        return "Disabled"

    def get_battery_percentage(self):
        return self.battery_level * 100

    def determine_flight_range(self):
        """
        Dummy method to determine how far the drone can go.
        """
        p_per_kg = 170  # Assume a conservative estimate of 170,000 W/g
        discharge = 0.8  # Assume a battery discharge of 80% during the flight.
        aad = (self.drone_weight_g / 1000) * (p_per_kg / float(self.battery_voltage))  # Calculate the average amp draw AAD = AUW * (P / V)
        flight_time_hrs = (self.battery_capacity_mAh / 1000) * discharge * aad  # time = capacity × discharge / AAD
        return flight_time_hrs * 100 / 2  # Max travel distance = time * kph / 2(round-trip)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    menu_items = models.ManyToManyField('MenuItem', related_name='categories')
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    options = models.ManyToManyField('MenuOption', related_name='menu_items')
    enabled = models.BooleanField(default=True)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class MenuOption(models.Model):
    DISPLAY_CHOICES = (
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio'),
    )

    name = models.CharField(max_length=255)
    display_type = models.CharField(max_length=10, choices=DISPLAY_CHOICES)
    values = models.ManyToManyField('OptionValue', related_name='menu_option')
    min_amount = models.PositiveIntegerField(default=0)
    max_amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class OptionValue(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, blank=True, null=True)
    items = models.JSONField()
    status = models.CharField(max_length=255, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.status}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField('MenuItem', through='CartItem')

    def __str__(self):
        return f"{self.user.get_full_name()}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    options = models.ManyToManyField('OptionValue', through='CartItemOption')

    def __str__(self):
        return f"{self.menu_item.name}"


class CartItemOption(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    option_value = models.ForeignKey('OptionValue', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.option_value.name}"
