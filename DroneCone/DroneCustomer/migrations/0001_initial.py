# Generated by Django 4.1.6 on 2023-11-28 15:16

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('qty', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('size', models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='small', max_length=10)),
                ('drone_weight_g', models.PositiveIntegerField()),
                ('battery_capacity_mAh', models.PositiveIntegerField()),
                ('battery_voltage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('battery_level', models.DecimalField(decimal_places=2, max_digits=3)),
                ('hours_worked', models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=4)),
                ('dollar_revenue', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('enabled', models.BooleanField(default=True)),
                ('in_flight', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drone', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IceCream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.CharField(max_length=127)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('qty', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Ice cream',
            },
        ),
        migrations.CreateModel(
            name='Markup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('markup_percentage', models.DecimalField(decimal_places=2, default=Decimal('10.0'), max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('qty', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cones', models.JSONField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('preparing', 'Preparing'), ('delivering', 'Delivering'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='Pending', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('drone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DroneCustomer.drone')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IceCreamCone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='small', max_length=10)),
                ('cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneCustomer.cone')),
                ('flavor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneCustomer.icecream')),
                ('toppings', models.ManyToManyField(blank=True, to='DroneCustomer.topping')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cones', models.ManyToManyField(blank=True, to='DroneCustomer.icecreamcone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
