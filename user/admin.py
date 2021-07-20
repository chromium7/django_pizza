from django.contrib import admin
from .models import Address, Order

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'address', 'price', 'created', 'active']
    list_filter = ['active']
    search_fields = ['buyer']
    date_hierarchy = 'created'
    ordering = ['active', 'created']