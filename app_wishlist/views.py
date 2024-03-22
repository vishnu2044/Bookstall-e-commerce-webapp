from django.shortcuts import render, redirect
from .models import Wishlist
from app_products.models import Product
from django.contrib import messages
from app_home.views import *


# Create your views here.
def wishlist_view(request):
    try:

        user = request.user
        if user.is_authenticated:
            
            wishlist_items = Wishlist.objects.filter(user = user)

            context = {
                'wishlist_items' : wishlist_items,
            }

            return render(request, 'temp_home/wishlist.html', context)
        else:
            messages.error(request, 'you need to login first!')
            return redirect(home)
        
    except:
        messages.warning(request, 'Oops something went wrong!')
        return redirect(home)



def add_to_wishlist(request, id):
    try:

        user = request.user
        if user.is_authenticated:
            product = Product.objects.get(id=id)
            user = request.user
                    
            if Wishlist.objects.filter(user=user, product=product).exists():
                messages.info(request, f' "{product.product_name}" is already in the wishlist!')
                referring_url = request.META.get('HTTP_REFERER')

                if referring_url:
                    return redirect(referring_url)
                else:
                    return redirect(wishlist_view)
            else:
                wishlist_item = Wishlist.objects.create(user=request.user, product=product)
                wishlist_item.save()
                messages.success(request, f" '{ product.product_name }' Added to wishlist successfully!")

            # Get the referring URL
                referring_url = request.META.get('HTTP_REFERER')

                if referring_url:
                    return redirect(referring_url)
                else:
                    return redirect(wishlist_view)
        else:
            messages.error(request, 'You need to login to add item in wishlist')
            referring_url = request.META.get('HTTP_REFERER')
            if referring_url:
                return redirect(referring_url)
            else:
                return redirect(home)
            
    except:
        messages.warning(request, 'Oops something went wrong!')
        return redirect(home)


def remove_from_wishlist(request, id):
    try:
        
        if request.user.is_authenticated:

            product = Product.objects.get(id=id)
            user = request.user
            wishlist_item = Wishlist.objects.get(product = product)
            if wishlist_item :
                wishlist_item.delete()
                messages.success(request, f'{product.product_name} romved from Wishlist')

                # Get the referring URL
                referring_url = request.META.get('HTTP_REFERER')
                if referring_url:
                    return redirect(referring_url)
                else:
                    return redirect(wishlist_view)

            else:
                messages.warning(request, f"{product.product_name} not present in wishlist")

                # Get the referring URL
                referring_url = request.META.get('HTTP_REFERER')
                if referring_url:
                    return redirect(referring_url)
                else:
                    return redirect(wishlist_view)
        else:
            messages.error(request, 'you need to login first')
            return redirect(home)
        
    except:
        messages.warning(request, 'Oops something went wrong!')
        return redirect(home)

