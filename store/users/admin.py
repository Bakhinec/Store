from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)


