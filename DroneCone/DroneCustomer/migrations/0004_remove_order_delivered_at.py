# Generated by Django 4.2.6 on 2023-11-10 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DroneCustomer', '0003_order_delivered_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivered_at',
        ),
    ]
