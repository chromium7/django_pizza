from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm

from menu.models import Pizza

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        product = get_object_or_404(Pizza, id=product_id)
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:detail')
    

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizza, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')