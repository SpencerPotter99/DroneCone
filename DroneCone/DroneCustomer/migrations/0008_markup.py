# Generated by Django 4.1.6 on 2023-11-27 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DroneCustomer', '0007_remove_drone_minutes_worked_drone_hours_worked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Markup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('markup_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
