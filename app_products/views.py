from django.shortcuts import redirect, render
from .models import *
from app_home.views import home
from app_order.models import OrderItem
from django.contrib import messages
from app_store.views import product_details

# Create your views here.
def user_product_review(request, product_id):
    try:
        if request.user.is_authenticated:

            current_user = request.user
            order_item = OrderItem.objects.filter(user=current_user, product=product_id)
            
            if order_item:
                product = Product.objects.get(id = product_id)
                if request.method == "POST":
                    review = request.POST.get('review')
                    rating = request.POST.get('rating')
                    if rating == "":
                        messages.warning(request, 'you need to give a rating for the product !')
                        return redirect('product_details', id=product_id)
                    
                    ProductReview.objects.create(
                            product = product,
                            user = current_user,
                            rating = rating,
                            text = review,
                    )
                    return redirect('product_details', id=product_id)
                
            else:
                messages.warning(request, 'you cant review this prodcut please buy the product first!')
                return redirect('product_details', id=product_id)

        return redirect(home)
    except:
        messages.warning(request, 'Oops something went wrong!')
        return redirect(home)