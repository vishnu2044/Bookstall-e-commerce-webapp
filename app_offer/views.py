from django.shortcuts import render, redirect
from .models import Offer
from django.contrib import messages
from app_admin_panel.views import admin_dashboard


# Create your views here.
def offers_list(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            offers = Offer.objects.all()
            context = {
                'offers': offers,
            }
            return render(request, 'adminpanel/offers_list.html', context)
        
        else:
            messages.error(request, 'Only admin can access this page !')
            return render(request, 'adminpanel/admin_login.html')  
    except:
        messages.warning(request, 'Oops! something went wrong!')
        return redirect(admin_dashboard)


def add_offer(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            if request.method == "POST":
                offer_name = request.POST.get('offer_name')
                off_percent = request.POST.get('off_percent')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')

                if off_percent is None:
                    messages.error(request, 'add off percentage')
                    return redirect(add_offer)

                if not offer_name.strip():
                    messages.error(request, 'add offer name!')
                    return redirect(add_offer)
            
                if start_date == "" or end_date == "":
                    messages.error(request, 'Give the dates frst!')
                    return redirect(add_offer)
                
                offer = Offer.objects.create(
                    name = offer_name,
                    off_percent = off_percent,
                    start_date = start_date,
                    end_date = end_date,
                )
                offer.save()
                messages.success(request, f'Offer "{offer_name} created successfully!')
                return redirect(offers_list)

            return render(request, 'adminpanel/add_new_offer.html')
        
        else:
            messages.error(request, 'Only admin can access this page !')
            return render(request, 'adminpanel/admin_login.html')  
    except:
        messages.warning(request, 'Oops! something went wrong!')
        return redirect(admin_dashboard)



def edit_offer(request, id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            if request.method == "POST":
                offer_name = request.POST.get('offer_name')
                off_percent = request.POST.get('off_percent')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
            
                if off_percent is None:
                    messages.error(request, 'add off percentage')
                    return redirect(add_offer)

                if not offer_name.strip():
                    messages.error(request, 'add offer name!')
                    return redirect(add_offer)
                if start_date == "" or end_date == "":
                    messages.error(request, 'Give the dates frst!')
                    return redirect(add_offer)
                
                Offer.objects.filter(id=id).update(
                    name = offer_name,
                    off_percent = off_percent,
                    start_date = start_date,
                    end_date = end_date,
                )
                messages.success(request, f'Offer "{offer_name} updated successfully!')
                return redirect(offers_list)
            
            try:
                offer = Offer.objects.get(id=id)
            except Offer.DoesNotExist:
                messages.error(request, 'Offer  does not exist.')
                return redirect(offers_list)
            context = {
                'offer': offer
            }
                
            return render(request, 'adminpanel/edit_offer.html', context)
        
        else:
            messages.error(request, 'Only admin can access this page !')
            return render(request, 'adminpanel/admin_login.html')  
    except:
        messages.warning(request, 'Oops! something went wrong!')
        return redirect(admin_dashboard)

