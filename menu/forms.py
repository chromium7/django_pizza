from django import forms

from .models import Pizza, Topping

PIZZA_SIZE_CHOICES = [
    ('s', 'Small'),
    ('m', 'Medium'),
    ('b', 'Big'),
]

class PizzaForm(forms.ModelForm):
    toppings = forms.ModelMultipleChoiceField(queryset=Topping.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Pizza
        fields = ('size', 'toppings')
        widgets = {
            'size': forms.Select(choices=PIZZA_SIZE_CHOICES),
        }