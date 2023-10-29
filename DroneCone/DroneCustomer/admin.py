from django.contrib import admin
from .models import MenuItem, MenuOption, OptionValue
# Register your models here.

admin.site.register(MenuOption)
admin.site.register(MenuItem)
admin.site.register(OptionValue)