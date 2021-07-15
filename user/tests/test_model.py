import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import Address, Order

class UserExtensionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password")
        self.address = Address.objects.create(street="test street", user=self.user)

    def test_order_ordering(self):
        now = timezone.now()
        hour_ago = now - datetime.timedelta(hours=1)
        first_order = Order.objects.create(buyer=self.user, address=self.address, created=hour_ago, price=1)
        second_order = Order.objects.create(buyer=self.user, address=self.address, price=1)

        orders = list(Order.objects.all())
        self.assertEqual(orders[0], first_order)
        self.assertEqual(orders[1], second_order)

    def test_order_url(self):
        order = Order.objects.create(buyer=self.user, address=self.address, price=1)
        self.assertEqual(order.get_absolute_url(), "/user/order/%s/" % order.id)

    def test_order_price_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            Order.objects.create(buyer=self.user, address=self.address, price="")

    def test_address_belongs_to_user(self):
        self.assertEqual(self.address.user, self.user)
    
    def test_address_str(self):
        self.assertEqual(str(self.address), "test street")