from django.contrib.auth.models import User
from django.test import TestCase

from menu.tests.factories import PizzaFactory

class CartViewTest(TestCase):
    
    def setUp(self) -> None:
        self.pizza = PizzaFactory()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_cart_view_renders_cart_template(self):
        response = self.client.get('/cart/')
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
    
    def test_cart_detail_is_initially_empty(self):
        response = self.client.get('/cart/')
        self.assertContains(response, 'Cart is empty.')

    def test_add_to_cart(self):
        data = {
            'quantity': 1,
            'override': False,
        }
        response = self.client.post(f'/cart/add/{self.pizza.id}/', data, follow=True)
        self.assertRedirects(response, '/cart/')
        self.assertEqual(len(response.context['cart']), 1)
        
    def test_remove_from_cart(self):
        data = {
            'quantity': 1,
            'override': False,
        }
        self.client.post(f'/cart/add/{self.pizza.id}/', data, follow=True)
        response = self.client.post(f'/cart/remove/{self.pizza.id}/', follow=True)
        self.assertRedirects(response, '/cart/')
        self.assertEqual(len(response.context['cart']), 0)

