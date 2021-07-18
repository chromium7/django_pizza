import factory
from ..models import Topping, ToppingType, Pizza

class ToppingTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ToppingType

    name = 'sauce'


class ToppingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topping

    name = 'tomato'
    price = 1
    type = factory.SubFactory(ToppingTypeFactory)


class PizzaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pizza

    size = 's'
    price = 4
    
    @factory.post_generation
    def toppings(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for topping in extracted:
                self.toppings.add(topping)

