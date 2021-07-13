from django.contrib import admin
from .models import Pizza, Topping, ToppingType


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['size', 'get_toppings', 'total_price']
    
    def get_toppings(self, obj):
        return ", ".join([topping.name for topping in obj.toppings.all()])
    get_toppings.short_description = 'Toppings'


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass


@admin.register(ToppingType)
class ToppingTypeAdmin(admin.ModelAdmin):
    pass