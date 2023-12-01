from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal


class Markup(models.Model):
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.0'))

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.markup_percentage}%"


class Drone(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="drone")
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='small')

    drone_weight_g = models.PositiveIntegerField()
    battery_capacity_mAh = models.PositiveIntegerField()
    battery_voltage = models.DecimalField(max_digits=5, decimal_places=2)
    battery_level = models.DecimalField(max_digits=3, decimal_places=2)  # 1.0 - 0.0
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    dollar_revenue = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    enabled = models.BooleanField(default=True)
    in_flight = models.BooleanField(default=False)

    def is_available(self):
        return self.enabled and not self.in_flight

    def get_drone_status(self):
        if self.enabled:
            return "Available" if not self.in_flight else "In Flight"
        return "Disabled"

    def __str__(self):
        return f"{self.name}"


class IceCream(models.Model):
    flavor = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    qty = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Ice cream"

    def __str__(self):
        return f"{self.flavor}"


class Topping(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Cone(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class IceCreamCone(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='small')
    flavor = models.ForeignKey('IceCream', on_delete=models.CASCADE)
    toppings = models.ManyToManyField('Topping', blank=True)
    cone = models.ForeignKey('Cone', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.flavor} | {self.cone} | {self.size} | {[str(topping) for topping in list(self.toppings.all())]}"

    def get_cone_info(self):
        return {'size': str(self.size),
                'flavor': str(self.flavor),
                'toppings': [str(topping) for topping in list(self.toppings.all())],
                'cone': str(self.cone),
                'price': str(self.get_price())}

    def get_price(self):
        price = self.cone.price + sum(topping.price for topping in self.toppings.all())
        match self.size:
            case 'small':
                price += self.flavor.price * 1
            case 'medium':
                price += self.flavor.price * 2
            case 'large':
                price += self.flavor.price * 3
        return price


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.SET_NULL, blank=True, null=True)
    cones = models.JSONField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.status}"

    def get_order_total(self):
        total_price = Decimal('0.00')
        cone_data_list = self.cones if isinstance(self.cones, list) else [self.cones]

        for cone_data in cone_data_list:
            cone_price = Decimal(cone_data.get('price', '0.00'))
            total_price += cone_price

        return total_price

    def get_cone_info(self):
        # Check if `self.cones` is a list of dictionaries (JSON data)
        if isinstance(self.cones, list):
            return self.cones
        # If `self.cones` is a single dictionary, return it inside a list
        elif isinstance(self.cones, dict):
            return [self.cones]
        # If `self.cones` is neither, return an empty list
        else:
            return []

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    cones = models.ManyToManyField('IceCreamCone', blank=True)

    def remove_all_cones(self):
        self.cones.clear()

    def get_cones_info(self):
        return [cone.cone_to_json() for cone in self.cones.all()]

    def __str__(self):
        return f"{self.user.username}'s cart"
