from django.shortcuts import render
from app_products.models import *
from app_cart.models import CartItem
# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    authors = Authors.objects.all()
    context = {
        "products_slides": products,
        "products": products[:3],
        "popular_products" : products[:6],
        "authors" : authors,
  
    }
    return render(request, "temp_home/home.html",context)

 
def about(request):
    return render(request, "temp_home/about.html")
 
 
def error_404_home(request):
    return render(request, 'temp_home/error-404-home.html')



