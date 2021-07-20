"""
    Models for pizza tables
    One pizza object can have several toppings
    Each topping has its own specific type
        e.g. Sauce = [Tomato, Chilli]
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField

class ToppingType(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    type = models.ForeignKey(ToppingType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.capitalize()


class Pizza(models.Model):    
    size = models.CharField(max_length=1)
    price = models.IntegerField()
    toppings = models.ManyToManyField(Topping)
    toppings_array = ArrayField(base_field=models.CharField(max_length=64), blank=True, null=True)

    def __str__(self):
        if self.size == 's':
            size = 'Small'
        elif self.size == 'm':
            size = 'Medium'
        else:
            size = 'Large'
        toppings = ", ".join([topping.name for topping in self.toppings.all()])
        return f"{toppings.capitalize()} ({size})"

    def total_price(self):
        toppings_price = sum([topping.price for topping in self.toppings.all()])
        return self.price + toppings_price