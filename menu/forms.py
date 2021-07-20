from django import forms

from .models import Pizza, Topping, ToppingType

PIZZA_SIZE_CHOICES = [
    ('s', 'Small'),
    ('m', 'Medium'),
    ('b', 'Big'),
]

def get_choices():
    query = Topping.objects.all().order_by('type__name', 'name')
    choices = {}
    for q in query:
        topping_type = q.type.name
        name = q.name
        id = q.id
        if topping_type not in choices:
            choices[topping_type] = []
        choices[topping_type].append((id, name))
    res = [(key, tuple(choices[key])) for key in choices]
    return tuple(res)

class PizzaForm(forms.ModelForm):
    choices = get_choices()
    toppings = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Pizza
        fields = ('size', 'toppings')
        widgets = {
            'size': forms.Select(choices=PIZZA_SIZE_CHOICES),
        }