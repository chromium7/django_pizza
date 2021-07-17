from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from user.forms import AddressRegistrationForm, UserRegistrationForm
from .models import Order

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(buyer=user)
    return render(request, 'user/profile.html', {'orders': orders})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    order = order.filter(buyer=request.user)
    return render(request, 'user/order.html', {'order': order})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, prefix="user_form")
        address_form = AddressRegistrationForm(request.POST, prefix="address_form")
        if user_form.is_valid() and address_form.is_valid():
            # Create new user instance
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Add user to address instance
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            return redirect(reverse('shop:home'))
    else:
        user_form = UserRegistrationForm(prefix="user_form")       
        address_form = AddressRegistrationForm(prefix="address_form")
    return render(request, 'registration/register.html', {'user_form': user_form, 'address_form': address_form})