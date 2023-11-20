# Generated by Django 4.2.7 on 2023-11-19 00:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DroneCustomer', '0006_remove_drone_hours_worked_drone_minutes_worked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drone',
            name='minutes_worked',
        ),
        migrations.AddField(
            model_name='drone',
            name='hours_worked',
            field=models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=4),
        ),
    ]
