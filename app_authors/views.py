from django.shortcuts import render, redirect
from django.contrib import messages
from app_authors.models import Authors
from app_products.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_admin_panel.views import admin_dashboard


# Create your views here.
#<<<<<<<<<<<<<<<< authors admin side >>>>>>>>>>>>>>>

def admin_authors(request):
    try:
        author = Authors.objects.all()

        per_page = 10
        page_number = request.GET.get('page')
        paginator = Paginator(author, per_page) 

        try:
            current_page = paginator.page(page_number)

        except PageNotAnInteger:
            current_page = paginator.page(1)

        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        return render(request, 'adminpanel/authors.html', {'current_page':current_page})
    except:
        messages.warning(request, 'oops somthing went worng!')
        return redirect(admin_dashboard)

def add_author_page(request):
    return render(request, 'adminpanel/add_author.html' )

def add_author(request):
    try:
        if request.method == "POST":
            image = ""
            try :
                image = request.FILES["image"]
            except:
                if image == "":
                    messages.info(request, "image field can't be empty")
                    return redirect(add_author)
            
            name = request.POST.get("name")
            nation = request.POST.get("nation")
            birthyear = request.POST.get("birthyear")
            quotes = request.POST.get("quotes")
            description = request.POST.get("description")
            check = [name, nation, birthyear, description]
            for values in check:
                if values == "":
                    messages.info(request, "some fields are empty")
                    return redirect(add_author) 
                else:
                    pass
            try:
                Authors.objects.get(author_name = name)
            except:
                Authors.objects.create(author_name = name,
                                    author_nation = nation,
                                    author_quotes = quotes,
                                    author_description = description,
                                    author_image = image,
                                    author_birth_year = birthyear,
                                    ).save()
                messages.success(request, f'Author "{name}" successfully added ! ')
                return redirect(admin_authors)
            else:
                messages.error(request, f'Author "{name}" already exist! ')
                return redirect(add_author)
        if not request.user.is_authenticated and not request.user.is_superuser:
            return redirect('admin_dashboard')

        
        
        authors = Authors.objects.all()
        context = {
            'authors': authors,
        }

        return render(request, 'adminpanel/add_author.html', context)
    except:
        messages.warning(request, 'oops somthing went worng!')
        return redirect(admin_dashboard)


def edit_author(request, id):
    try:
        if request.method == "POST":
            image = ""
            try :
                image = request.FILES["image"]
                print(image)
                author = Authors.objects.filter(id=id).first()
                author.author_image = image
                author.save()
            except:
                print("Hi")  
                
            name = request.POST.get('name')
            nation = request.POST.get('nation')
            birthyear = request.POST.get('birthyear')
            quotes = request.POST.get('quotes')
            description = request.POST.get('description')

            author = Authors.objects.filter(id=id).update(
                    author_name = name,
                    author_nation = nation,
                    author_quotes = quotes,
                    author_description = description,
                    author_birth_year = birthyear,
            )
            messages.success(request, f'{name} updated successfully!')
            return redirect(admin_authors)
        
        author = Authors.objects.get(id=id)
        context = {
            'author': author,
        }
        return render(request, 'adminpanel/edit_author.html', context)
    
    except:
        messages.warning(request, 'oops somthing went worng!')
        return redirect(admin_dashboard)



#<<<<<<<<<<<<<<<< authors user side >>>>>>>>>>>>>>>

def authors_page(request):
    try: 
        authors = Authors.objects.all()

        per_page = 2
        page_number = request.GET.get('page')
        paginator = Paginator(authors, per_page)

        try:
            current_page = paginator.page(page_number)

        except PageNotAnInteger:
            current_page = paginator.page(1)

        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context = {
            "authors": authors,
            "current_page": current_page,
        }
        return render(request, 'temp_home/authors_page.html', context)
    
    except:
        messages.warning(request, 'oops somthing went worng!')
        return redirect(admin_dashboard)

def author_books(request, id):
    try:
        products = Product.objects.filter(author=id)
        context = {'products': products}
        return render(request, 'temp_home/author_books.html', context)
    except:
        messages.warning(request, 'oops somthing went worng!')
        return redirect(admin_dashboard)


def search_authors(request):
    try:
        search_text = request.POST.get("query")
        authors = Authors.objects.filter(author_name__icontains = search_text)

        per_page = 2
        page_number = request.GET.get('page')
        paginator = Paginator(authors, per_page)
    
        try:
            current_page = paginator.page(page_number)

        except PageNotAnInteger:
            current_page = paginator.page(1)

        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context = {
            "authors": authors,
            "current_page": current_page,
        }
        return render(request, 'temp_home/authors_page.html', context)
    
    except:
        messages.warning(request, 'oops somthing went worng!')
        return redirect(admin_dashboard)