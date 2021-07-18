"""
    Models for pizza tables
    One pizza object can have several toppings
    Each topping has its own specific type
        e.g. Sauce = [Tomato, Chilli]
"""

from django.db import models


class ToppingType(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    type = models.ForeignKey(ToppingType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name.capitalize()} costs ${self.price}"


class Pizza(models.Model):    
    size = models.CharField(max_length=1)
    price = models.IntegerField()
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        if self.size == 's':
            size = 'Small'
        elif self.size == 'm':
            size = 'Medium'
        else:
            size = 'Large'
        toppings = ", ".join([topping.name for topping in self.toppings.all()])
        return f"{size} pizza with {toppings}"

    def total_price(self):
        toppings_price = sum([topping.price for topping in self.toppings.all()])
        return self.price + toppings_price