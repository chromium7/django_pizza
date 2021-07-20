from django.test import TestCase
from .factories import PizzaFactory, ToppingFactory, ToppingTypeFactory

class PizzaModelTest(TestCase):

    def setUp(self):
        self.sauce = ToppingTypeFactory.create()
        self.tomato = ToppingFactory.create(type=self.sauce)
        self.small_pizza = PizzaFactory.create(toppings=(self.tomato,))
        self.big_pizza = PizzaFactory.create(size="b", price=12, toppings=(self.tomato,))

    def test_tomato_is_related_to_sauce(self):
        self.assertIn(self.tomato, self.sauce.topping_set.all())

    def test_pizza_string(self):
        self.assertEqual(str(self.small_pizza), "Tomato (Small)")

    def test_pizza_base_price(self):
        self.assertEqual(self.small_pizza.total_price(), 5)
        self.assertEqual(self.big_pizza.total_price(), 13)
    
    