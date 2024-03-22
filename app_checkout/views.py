from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress
from django.contrib import messages
from app_cart.views import cart
from app_home.views import home

# Create your views here.
def checkout(request):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
            if cart_items is None:
                messages.warning(request, 'cart is empty !')
                return redirect(cart)
            for cart_item in cart_items:
                if cart_item.quantity > cart_item.product.stock:
                    print("cart item out of stock")
                    return redirect('cart')
            address = UserAddress.objects.filter(user=request.user)
            context = {
                'addresses': address
            }
            return render(request, 'temp_home/checkout.html', context)
        else:
            messages.error(request, 'you need to login for place a order')
            return redirect(home)
    except:
        messages.error(request, 'Oops something went worng!')
        return redirect(home)