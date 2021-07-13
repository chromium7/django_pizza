from django.contrib import admin
from .models import Address, Order

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
