from django.test import TestCase, RequestFactory
from django.conf import settings

from menu.tests.factories import PizzaFactory

from ..cart import Cart
from .helpers import SessionDict

class CartObjectTest(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.request.session = SessionDict()
        self.request.session.modified = False

        self.pizza = PizzaFactory()
        self.cart = Cart(self.request)
    
    def test_length_of_cart(self):
        self.assertEqual(len(self.cart), 0)

    def test_add_to_cart(self):
        self.cart.add(self.pizza, quantity=3)
        self.assertEqual(len(self.cart), 3)

    def test_override_quantity_cart(self):
        self.cart.add(self.pizza)
        self.assertEqual(len(self.cart), 1)
        self.cart.add(self.pizza, quantity=3, override_quantity=True)
        self.assertEqual(len(self.cart), 3)

    def test_iterate_cart(self):
        self.cart.add(self.pizza)
        for item in self.cart:
            self.assertEqual(item['product'], self.pizza)
            self.assertEqual(item['price'], 4)

    def test_remove_from_cart(self):
        self.cart.add(self.pizza)
        self.assertEqual(len(self.cart), 1)
        self.cart.remove(self.pizza)
        self.assertEqual(len(self.cart), 0)

    def test_total_price_of_cart(self):
        self.cart.add(self.pizza, quantity=3)
        self.assertEqual(self.cart.get_total_price(), 12)

    def test_clear_cart(self):
        self.cart.add(self.pizza, quantity=3)
        self.cart.clear()
        self.assertIsNone(self.request.session.get(settings.CART_SESSION_ID, None))