from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from user.forms import AddressSelectForm
from user.models import Order

from .models import Pizza, Topping
from .forms import PizzaForm

def index(request):
    pizza_form = PizzaForm()
    cart_form = CartAddProductForm()
    message = None

    if request.session.get('cart_success', False) == True:
        message = "Added to cart!"
        request.session['cart_success'] = False

    return render(request, 'menu/index.html', {
        'pizza_form': pizza_form,
        'cart_form': cart_form,
        'message': message
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
        topping_ids = [int(id) for id in pizza_data['toppings']]
        toppings = Topping.objects.filter(pk__in=topping_ids)
        toppings_name = [topping.name for topping in toppings]

        try:
            # Get pizza object
            pizza = Pizza.objects.get(size=size, price=price, toppings_array=toppings_name)
        except Pizza.DoesNotExist:
            pizza = Pizza.objects.create(size=size, price=price, toppings_array=toppings_name)
            pizza.toppings.add(*toppings)
            pizza.save()

        # Add pizza to the cart
        cart = Cart(request)
        cart.add(pizza, cart_data['quantity'], cart_data['override'])

        request.session['cart_success'] = True

    return redirect('menu:index')


@require_POST
def create_order(request):
    cart = Cart(request)
    address_form = AddressSelectForm(request.POST, user=request.user)
    if address_form.is_valid():
        order = Order.objects.create(
            buyer=request.user,
            address=address_form.cleaned_data['address'],
            price=cart.get_total_price()
        )
        order.pizza.add(*[item['product'] for item in cart])
        order.save()
        cart.clear()
        return redirect('user:profile')


def order_created(request):
    return render(request, 'menu/order_created.html')