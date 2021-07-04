from django.test import TestCase
from .models import Pizza, Topping, ToppingType

class PizzaModelTest(TestCase):

    def setUp(self):
        self.sauce = ToppingType.objects.create(name="sauce")
        self.tomato = Topping.objects.create(name="tomato", price=1, type=self.sauce)
        self.small_pizza = Pizza.objects.create(size="s", price=4)
        self.small_pizza.toppings.add(self.tomato)
        self.big_pizza = Pizza.objects.create(size="b", price=12)
        self.big_pizza.toppings.add(self.tomato)

    def test_tomato_is_related_to_sauce(self):
        self.assertIn(self.tomato, self.sauce.topping_set.all())

    def test_pizza_string(self):
        self.assertEqual(str(self.small_pizza), "Small pizza with tomato costs $5")

    def test_pizza_base_price(self):
        self.assertEqual(self.small_pizza.total_price(), 5)
        self.assertEqual(self.big_pizza.total_price(), 13)
    
    