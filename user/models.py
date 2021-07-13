"""
    Models for user related data
    Each user can have multiple addresses
    Each user can have multiple orders
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from menu.models import Pizza

class Address(models.Model):
    street = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.street


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"{self.buyer} ordered {self.pizza}"

    def get_absolute_url(self):
        return reverse("user:order", args=[self.id])
    