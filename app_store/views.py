from django.shortcuts import render, redirect
from app_products.models import *
from app_cart.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from app_authors.models import *


# Create your views here.
def shop(request):

    products = Product.objects.all().filter(is_available=True)
    products_ascending = Product.objects.all().filter(is_available=True).order_by('product_name')
    products_high_to_low = Product.objects.all().filter(is_available=True).order_by('price')

    cart_items = CartItem.objects.all()
    Categories = Category_list.objects.all()
    authors = Authors.objects.all()

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)
    paginator2 = Paginator(products_ascending, per_page)
    paginator3 = Paginator(products_high_to_low, per_page)

    try:
        current_page = paginator.page(page_number)
        current_page2 = paginator2.page(page_number)
        current_page3 = paginator3.page(page_number)
    
    except PageNotAnInteger:
        # If the 'page' parameter is not an integer, display the first page
        current_page = paginator.page(1)
        current_page2 = paginator2.page(1)
        current_page3 = paginator3.page(1)

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        current_page2 = paginator2.page(paginator.num_pages)
        current_page3 = paginator3.page(paginator.num_pages)

    context = {
        "current_page3": current_page3,
        "current_page2": current_page2,
        "current_page": current_page,
        "categories": Categories,
        "authors": authors,
        "products": products,
        "products_old_books" : products[3:],
        "products_popular" : products[2:5],
        "cart_items" : cart_items,
    }
    
    return render(request, 'temp_home/shop.html', context)


def product_details(request, id):
    product = Product.objects.get(id=id)
    product_reviews = ProductReview.objects.filter(product = product)
    count = 0
    total_review = 0
    for review in product_reviews:
        count += 1 
        total_review += review.rating
    if count != 0 :
        review_rate =  (total_review/count)
    else:
        review_rate = 0

    context = {
        "review_rate": review_rate,
        "product_reviews": product_reviews[:3],
        "product": product,
    }
    return render(request, 'temp_home/product_details.html', context)

def all_reviews(request, id):
    product = Product.objects.get(id=id)
    product_reviews = ProductReview.objects.filter(product = product)
    count = 0
    total_review = 0
    for review in product_reviews:
        count += 1 
        total_review += review.rating

    review_rate =  (total_review/count)

    context = {
        "product": product,
        "review_rate": review_rate,
        "product_reviews": product_reviews,
    }
    return render(request, 'temp_home/all_reviews.html', context)



def product_search(request):
    search_text = request.POST.get("query")
    products = Product.objects.filter(product_name__icontains=search_text)

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)

    try:
        current_page = paginator.page(page_number)
    
    except PageNotAnInteger:
        # If the 'page' parameter is not an integer, display the first page
        current_page = paginator.page(1)

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        
   
    context = {
        "current_page": current_page,
        "products": products,
        "search_text" : search_text,
    }
    return render(request, 'temp_home/shop.html', context)
    

def filtering_products(request):
    products = Product.objects.filter(is_available=True)
    authors = Authors.objects.all()
    categories = Category_list.objects.all()

    # Filtering products
    price_range = request.GET.get('price_range')
    category = request.GET.get('category')
    author = request.GET.get('author')

    category_obj, author_obj = None, None
    max_price, min_price = None, None

    if price_range:
        min_price, max_price = map(int, price_range.split("-"))
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if category:
        try:
            category_obj = Category_list.objects.get(category_name=category)
            products = products.filter(category=category_obj)
        except Category_list.DoesNotExist:
            pass

    if author:
        try:
            author_obj = Authors.objects.get(author_name=author)
            products = products.filter(author=author_obj)
        except Authors.DoesNotExist:
            pass

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)

    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    category_name, author_name = None, None
    mi_price, ma_price = None, None

    if min_price  and max_price:
        mi_price = min_price
        ma_price = max_price

    if category_obj:
        category_name = category_obj
    if author_obj:
        author_name = author_obj

    context = {
        "mi_price": mi_price,
        "ma_price": ma_price,
        "author_name": author_name,
        "category_name": category_name,
        "current_page": current_page,
        "authors": authors,
        "categories": categories,
        "products": products,
    }

    return render(request, 'temp_home/shop.html', context)

