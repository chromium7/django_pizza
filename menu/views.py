from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm

from .models import Pizza
from .forms import PizzaForm

def index(request):
    pizza_form = PizzaForm()
    cart_form = CartAddProductForm()
    return render(request, 'menu/index.html', {
        'pizza_form': pizza_form,
        'cart_form': cart_form,
    })


@require_POST
def add_to_cart(request):
    pizza_form = PizzaForm(request.POST)
    cart_form = CartAddProductForm(request.POST)
    if pizza_form.is_valid() and cart_form.is_valid():
        pizza_data = pizza_form.cleaned_data
        cart_data = cart_form.cleaned_data

        # Validate pizza size
        size = pizza_data['size']
        if size == 's':
            price = 4
        elif size == 'm':
            price = 8
        elif size == 'b':
            price = 12
        else:
            # If pizza size is invalid
            # re-render the form with error messages
            return render(request, 'menu/index.html', {
                'pizza_form': pizza_form,
                'cart_form': cart_form,
                'error_message': 'Pizza size is invalid',
            })
        
        toppings_name = [topping.name for topping in pizza_data['toppings']]

        try:
            # Get pizza object
            pizza = Pizza.objects.get(size=size, price=price, toppings_array=toppings_name)
        except Pizza.DoesNotExist:
            pizza = Pizza.objects.create(size=size, price=price, toppings_array=toppings_name)
            pizza.toppings.add(*pizza_data['toppings'])
            pizza.save()

        # Add pizza to the cart
        cart = Cart(request)
        cart.add(pizza, cart_data['quantity'], cart_data['override'])

    return redirect('menu:index')