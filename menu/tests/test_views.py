from django.test import TestCase
from django.contrib.auth.models import User
from cart.forms import CartAddProductForm
from .factories import ToppingFactory, PizzaFactory
from ..forms import PizzaForm

class PizzaViewTest(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='test', password='test')

    def add_to_cart(self):
        topping1 = ToppingFactory()
        data = {
            'toppings': [topping1.id],
            'size': 'small',
            'quantity': 1
        }
        response = self.client.post('/menu/add/', data)
        return response

    def test_pizza_index_show_forms(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['pizza_form'], PizzaForm)
        self.assertIsInstance(response.context['cart_form'], CartAddProductForm)

    def test_add_to_cart_works(self):
        self.client.login(username='test', password='test')
        response = self.add_to_cart()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/menu/')
        
    def test_add_to_cart_require_login(self):
        response = self.add_to_cart()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/')