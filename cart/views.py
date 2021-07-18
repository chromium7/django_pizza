from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm

from menu.models import Pizza

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizza, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['override'])
        return redirect('cart:cart_detail')
    

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizza, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')