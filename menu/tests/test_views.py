from django.test import TestCase
from cart.forms import CartAddProductForm
from .factories import ToppingFactory
from ..forms import PizzaForm

class PizzaViewTest(TestCase):

    def test_pizza_index_show_forms(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['pizza_form'], PizzaForm)
        self.assertIsInstance(response.context['cart_form'], CartAddProductForm)

    def test_add_to_cart_works(self):
        pass