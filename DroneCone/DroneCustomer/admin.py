from django.contrib import admin
from .models import IceCream, IceCreamCone, Topping, Cone
# Register your models here.

admin.site.register(IceCream)
admin.site.register(IceCreamCone)
admin.site.register(Topping)
admin.site.register(Cone)