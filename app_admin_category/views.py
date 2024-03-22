from django.shortcuts import redirect, render
from django.contrib import messages
from app_category.models import Category_list
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from app_products.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin_panel.views import super_admincheck
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_offer.models import Offer


# Create your views here.
#<<<<<<<<<<<<<<<<<<<<<<<<<  to display categories list in admin side  >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def categories_list(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:   
            categories = Category_list.objects.all()

            per_page = 5
            page_number = request.GET.get('page')
            paginator = Paginator(categories, per_page)

            try:
                current_page = paginator.page(page_number)
            except PageNotAnInteger:
                current_page = paginator.page(1)

            except EmptyPage:
                current_page = paginator.page(paginator.num_pages)

            offers = Offer.objects.all()
            context = {
                'offers' : offers,
                'current_page' : current_page,
            }
            return render(request, 'adminpanel/categories.html', context)
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        return render(request, 'adminpanel/error-404-admin.html')


#<<<<<<<<<<<<<<<<<<<<<<<<<  add new  category to the category list   >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def add_category(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:   
            if request.method == "POST":
                name = request.POST.get('name')
                slug = request.POST.get('slug')
                descripiton = request.POST.get('description')
                offer = request.POST.get('offer_name')
                
                offer_id = None 
                if offer:
                    offer_id = Offer.objects.get(id=offer)
                check = [name, slug]
                is_available = request.POST.get('is_available', False)
                if is_available:
                    is_available = True
                else:
                    is_available = False
                for values in check:
                    if values == '':
                        messages.info(request, 'please enter both category name and slug !')
                        return redirect(add_category)
                    else:
                        pass
                try:
                    Category_list.objects.get(category_name = name )
                except:
                    Category_list.objects.create(
                                            category_name = name, 
                                            slug = slug , 
                                            category_description = descripiton,
                                            offer = offer_id,
                                            )
                    messages.success(request,f'Category "{name}" succesfully added')
                    return redirect(categories_list)
                else:
                    messages.error(request, f'category "{name} is already exist !')
                    return redirect(add_category)
                
            if not request.user.is_authenticated and not request.user.is_superuser:
                return redirect('admin_dashboard')
            categories = Category_list.objects.all()

            offers = Offer.objects.all()
            offers_active = []
            for offer in offers:
                if not offer.is_expired :
                    offers_active.append(offer)
                    
            context = {
                'offers' : offers_active,
                'categories' : categories,
            }
            return render(request, 'adminpanel/categories.html', context)
        
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        return render(request, 'adminpanel/error-404-admin.html')
    

#<<<<<<<<<<<<<<<<<<<<<<<<<  Edit the excisting category items    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def edit_catgory(request, id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:   

            if request.method == "POST":
                name = request.POST.get('name')
                slug = request.POST.get('slug')
                description = request.POST.get('description')
                offer = request.POST.get('offer_name')

                

                category = Category_list.objects.filter(id=id).update(
                            category_name = name,
                            slug = slug,
                            category_description = description,
                            offer = offer
                )
                messages.success(request, f'{name} updated successfully')

                return redirect(categories_list)

            try:
                category = Category_list.objects.get(id=id)
            except Category_list.DoesNotExist:
                messages.error(request, 'Category does not exist.')
                return redirect(categories_list)
            
            offers = Offer.objects.all()
            offers_active = []
            for offer in offers:
                if not offer.is_expired :
                    offers_active.append(offer)

            context = {
                "offers": offers_active,
                "category": category
            }
            return render(request, 'adminpanel/edit_category.html', context)
        
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
        
    except:
        return render(request, 'adminpanel/error-404-admin.html')


@login_required
@user_passes_test(super_admincheck)
def unlist_category(request, id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:   

            try:
                category = Category_list.objects.get(id=id)
            except ObjectDoesNotExist:
                messages.error(request, 'Category does not exist.')
                return redirect(add_category)

            name = category.category_name
            category.is_available = False
            category.save()
            messages.warning(request, f'Category "{name}" is unlisted.')
            return redirect(add_category)
        
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        return render(request, 'adminpanel/error-404-admin.html')
    


@login_required
@user_passes_test(super_admincheck)
def list_category(request, id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:   

            try:
                category = Category_list.objects.get(id=id)
            except ObjectDoesNotExist:
                messages.error(request, 'Category does not exist.')
                return redirect(add_category)

            name = category.category_name
            category.is_available = True
            category.save()
            messages.success(request, f'Category "{name}" is listed.')
            return redirect(add_category)
        
        else:
            messages.error(request, 'only admin can use this page !')
            return render(request, 'adminpanel/admin_login.html')
    except:
        return render(request, 'adminpanel/error-404-admin.html')