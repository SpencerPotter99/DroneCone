<<<<<<< HEAD
# Generated by Django 4.2.6 on 2023-10-28 21:55
=======
# Generated by Django 4.2.6 on 2023-10-28 01:13
>>>>>>> e7180db0a032a4379f5905941f726cc13ff5e605

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
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
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
                ('battery_level', models.DecimalField(decimal_places=1, max_digits=2)),
                ('enabled', models.BooleanField(default=True)),
                ('in_flight', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='IceCream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.CharField(max_length=127)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('qty', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('qty', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cones', models.JSONField()),
                ('status', models.CharField(default='Pending', max_length=255)),
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
                ('qty', models.PositiveSmallIntegerField(default=1)),
                ('cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneCustomer.cone')),
                ('flavor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneCustomer.icecream')),
                ('toppings', models.ManyToManyField(to='DroneCustomer.topping')),
            ],
        ),
        migrations.CreateModel(
            name='DroneOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drones', models.ManyToManyField(related_name='owner', to='DroneCustomer.drone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='drone_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cones', models.ManyToManyField(to='DroneCustomer.icecreamcone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
