from django.test import TestCase, RequestFactory

from menu.tests.factories import PizzaFactory

from ..cart import Cart
from .helpers import SessionDict

class CartViewsTest(TestCase):
    def setUp(self):
        request = RequestFactory()
        request.session = SessionDict()
        request.session.modified = False

        self.pizza = PizzaFactory()
        self.cart = Cart(request)