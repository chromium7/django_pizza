from django import forms

from .models import Pizza, Topping, ToppingType

PIZZA_SIZE_CHOICES = [
    ('s', 'Small ($4)'),
    ('m', 'Medium ($8)'),
    ('b', 'Big ($12)'),
]

def get_choices():
    query = Topping.objects.all().order_by('type__name', 'name')
    choices = {}
    for q in query:
        topping_type = q.type.name.capitalize()
        if topping_type not in choices:
            choices[topping_type] = []
        choices[topping_type].append((q.id, f"${q.price} > {q.name.capitalize()}"))
    res = [(key, tuple(choices[key])) for key in choices]
    return tuple(res)

class PizzaForm(forms.ModelForm):
    choices = get_choices()
    toppings = forms.MultipleChoiceField(
        choices=choices, 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'topping-checkbox'}),    
    )

    class Meta:
        model = Pizza
        fields = ('size', 'toppings')
        widgets = {
            'size': forms.Select(choices=PIZZA_SIZE_CHOICES),
        }