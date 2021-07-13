from django.shortcuts import render, get_object_or_404

from .models import Order

def order_detail(request, id):
    order = get_object_or_404(Order, id=id, buyer=request.user)
    return render(request, 'user/order.html', {'order': order})