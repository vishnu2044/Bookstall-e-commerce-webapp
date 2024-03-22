from django.shortcuts import redirect, render
from django.contrib import messages
from app_category.models import Category_list
from django.core.exceptions import ObjectDoesNotExist
from app_products.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin_panel.views import super_admincheck
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_admin_category.views import add_category

# Create your views here

#<<<<<<<<<<<<<<<<<<<<<<<<<  to display all prodcuts in the admin side    >>>>>>>>>>>>>>>>>>>>>>>>>
def admin_products(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            products = Product.objects.all()

            per_page = 5
            page_number = request.GET.get('page')
            paginator = Paginator(products, per_page)

            try:
                current_page = paginator.page(page_number)

            except PageNotAnInteger:
                current_page = paginator.page(1)
            except EmptyPage:
                current_page = paginator.page(paginator.num_pages)
            
            context = {
                "current_page" : current_page,
            }
            return render(request, 'adminpanel/products_list.html', context)
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        messages.warning(request, 'oops something went wrong')
        return redirect(admin_products)

#<<<<<<<<<<<<<<<<<<<<<<<<<  to redirect to add product page    >>>>>>>>>>>>>>>>>>>>>>>>>
def add_product_page(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, 'adminpanel/add_product.html')
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        messages.warning(request, 'oops something went wrong')
        return redirect(admin_products)

 
def add_product(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            if request.method == "POST":
                image = ''
                try:
                    image = request.FILES["image"]
                except:
                    if image == '':
                        messages.info(request, "Image field cant't be empty !")
                        return redirect(add_product)

                name = request.POST.get("name")
                slug = request.POST.get("slug")
                price = request.POST.get("price")
                stock = request.POST.get("stock")
                category = request.POST.get("category")
                author = request.POST.get("author")
                offer = request.POST.get('offer_name')
                description = request.POST.get("description")

                if len(name) == 0:
                    messages.warning(request, 'please enter the product name')
                    return redirect(add_product)

                if author == "":
                    messages.warning(request, 'please select an author.')
                    return redirect(add_product)

                if category == "":
                    messages.warning(request, 'please select a category.')
                    return redirect(add_product)


                try:
                    if Product.objects.get(slug=slug):
                        messages.info(request, "Product with this slug already exists!")
                        return redirect(add_product)
                except Product.DoesNotExist:
                    pass

                check = [name, slug, price, stock, description]
                for values in check:
                    if values == "":
                        messages.info(request, "Some fields are empty!")
                        return redirect(add_product)

                author_instance = Authors.objects.get(id=author)
                category_instance = Category_list.objects.get(id=category)
                offer_instance = None
                if offer:
                    offer_instance = Offer.objects.get(id=offer)

                Product.objects.create(
                    product_name=name,
                    slug=slug,
                    product_description=description,
                    price=price,
                    stock=stock,
                    images=image,
                    category=category_instance,
                    author=author_instance,
                    offer=offer_instance
                )
                print("product created>>>>>>>>>>>>>>>>>>>>>>>>>")
                messages.success(request, f'Book : {name} added successfully')
                return redirect(admin_products)

            authors = Authors.objects.all()
            categories = Category_list.objects.all()

            offers = Offer.objects.all()
            offers_active = [offer for offer in offers if not offer.is_expired]
            print("***************************** offers active :::::::::::::", offers_active)

            context = {
                'offers': offers_active,
                'categories': categories,
                'authors': authors,
            }
            return render(request, 'adminpanel/add_product.html', context)

        else:
            messages.error(request, 'Only admin can use this page!')
            return render(request, 'adminpanel/admin_login.html')

    except Exception as e:
        print(e)
        messages.warning(request, 'Oops! Something went wrong')
        return redirect(admin_products)



def admin_search_prodcuts(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:

            if request.method == "GET":
                query = request.GET.get("query")
                if query:
                    detail = Product.objects.filter(product_name=query)
                    detail = Product.objects.filter(slug=query)
                    return render(request, 'adminpanel/searchproduct.html', {"details" : detail})
                else:
                    return render(request, 'admin_panel/search.html', {})
                
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        messages.warning(request, 'oops something went wrong')
        return redirect(admin_products)
    
    


#<<<<<<<<<<<<<<<<<<<<<<<<<  Edit the excisting product details    >>>>>>>>>>>>>>>>>>>>>>>>>


@login_required
@user_passes_test(super_admincheck)
def edit_product(request, id):
    try:
        if id:
            print('id:::::::::::::::', id)
        else:
            print("no id present ")
        if request.user.is_authenticated and request.user.is_superuser:
            if request.method == 'POST':
                image = ''
                try:
                    image = request.FILES["image"]
                    product = Product.objects.filter(id=id).first()
                    product.images = image
                    product.save()
                except Exception as e:
                    print("Error at image:", e)
        
                
                name = request.POST.get("name")
                slug = request.POST.get("slug")
                price = request.POST.get("price")
                stock = request.POST.get("stock")
                category = request.POST.get("category")
                author = request.POST.get("author")
                description = request.POST.get("description")
                offer = request.POST.get("offer_name")

                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print("\n name ::::::::", name,
                      "\n slug ::::::::", slug,
                      "\n price ::::::::", price,
                      "\n stock ::::::::", stock,
                      "\n category ::::::::", category,
                      "\n author ::::::::", author,
                      "\n description ::::::::", description,
                      "\n offer ::::::::", offer,
                       )
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                if name == "":
                    messages.error(request, "Product name can't be null!")
                    return redirect(edit_product, id=id)
                print("")
                author_instance = Authors.objects.filter(id=author).first()
                categoriy_instance = Category_list.objects.filter(id=category).first()
                if offer:
                    offer_instance = Offer.objects.filter(id=offer).first()
                else:
                    print("no offer id")
                    offer_instance = None       

                Product.objects.filter(id=id).update(
                            product_name = name,
                            slug = slug,
                            product_description = description,
                            price = price,
                            stock = stock,
                            author = author_instance,
                            category = categoriy_instance,
                            offer = offer_instance,
                    )
                messages.success(request, f'{name} updated successfully!')
                return redirect(admin_products)
            
            product = Product.objects.get(id=id)
            categories = Category_list.objects.all()
            authors = Authors.objects.all()

            offers = Offer.objects.all()
            offers_active = [offer for offer in offers if  offer.is_expired]

            print('offers', offers)
            if offers_active:
                for offr in offers_active:
                    print(
                        "\n name ::::::::", offr.name,
                        "\n start date ::::::::", offr.start_date,
                        "\n end_date ::::::::", offr.end_date,
                        
                        )
            else:
                print("no offers are active>>>>>>>>>>>>>>>>>>>>>>>>")
                    
            context = {
                "offers": offers_active,
                "product": product,
                "categories" : categories,
                "authors" : authors,
            }
            return render(request, 'adminpanel/edit_product.html', context)
        else:
            messages.error(request, 'Only admin can use this page!')
            return render(request, 'adminpanel/admin_login.html')   
           
    except Exception as e:
        messages.warning(request, 'Oops something went wrong')
        print("Error:", e)
        return redirect(admin_products)




#<<<<<<<<<<<<<<<<<<<<<<<<<  unlist the excisting prodcut details    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def unlist_product(request, id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:    
            try:
                product = Product.objects.get(id=id)
            except ObjectDoesNotExist:
                messages.error(request, 'Product does not exist.')
                return redirect(add_category)

            name = product.product_name
            product.is_available = False
            product.save()
            messages.warning(request, f'Product "{name}" is unlisted.')
            return redirect(admin_products)
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')  
    except:
        messages.warning(request, 'oops something went wrong')
        return redirect(admin_products)
    

#<<<<<<<<<<<<<<<<<<<<<<<<<  list the excisting prodcut details    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def list_product(request, id):  
    try:
        if request.user.is_authenticated and request.user.is_superuser:    

            try:
                product = Product.objects.get(id=id)
            except ObjectDoesNotExist:
                messages.error(request, 'Product does not exist.')
                return redirect(add_category)

            name = product.product_name
            product.is_available = True
            product.save()
            messages.warning(request, f'Product "{name}" is listed.')
            return redirect(admin_products)
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
        
    except:
        messages.warning(request, 'oops something went wrong')
        return redirect(admin_products)
    



def admin_product_reviews(request, id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:    

            reviews = ProductReview.objects.filter(product = id)
            
            per_page = 10
            page_number = request.GET.get('page')
            paginator = Paginator(reviews, per_page) 

            try:
                current_page = paginator.page(page_number)

            except PageNotAnInteger:
                current_page = paginator.page(1)

            except EmptyPage:
                current_page = paginator.page(paginator.num_pages)
                context = {
                    'reviews': current_page
                }
                return render(request, 'adminpanel/user_reviews_admin.html', context)
            return redirect(admin_products)
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
        
    except:
        messages.warning(request, 'oops something went wrong')
        return redirect(admin_products)
    