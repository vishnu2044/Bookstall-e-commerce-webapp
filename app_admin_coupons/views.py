from django.shortcuts import render, redirect
from app_offer.models import Coupon
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin_panel.views import super_admincheck



# Create your views here.
@login_required
@user_passes_test(super_admincheck)
def coupons_list(request):
    try:
        coupons = Coupon.objects.all()
        context = {
            'coupons': coupons,
        }
        return render(request, 'adminpanel/coupon_list.html', context)
    except:
        return render(request, 'adminpanel/error-404-admin.html')



@login_required
@user_passes_test(super_admincheck)
def add_coupon(request):
    try:
        if request.method == "POST":
            coupon_code = request.POST.get("coupon_code")
            min_amount = request.POST.get("min_amount")
            off_percent = request.POST.get("off_percent")
            max_discount = request.POST.get("max_discount")
            expiry_date_str = request.POST.get("expairy_date")

            print("***************************************",expiry_date_str,"***********************")

            # Validate coupon_code
            if coupon_code and coupon_code.islower():
                messages.warning(request, "Coupon code cannot contain small letters!")
                return redirect("add_coupon")
            
            if Coupon.objects.filter(coupon_code=coupon_code).exists():
                messages.warning(request, "this coupon is already in your account!")
                return redirect("add_coupon")

            # Validate min_amount
            if not min_amount.isdigit() or int(min_amount) < 500:
                messages.warning(request, "Minimum amount must be a number greater than or equal to 500!")
                return redirect("add_coupon")

            # Validate off_percent
            if not off_percent.isdigit() or int(off_percent) <= 0:
                messages.warning(request, "Off percent must be a positive number greater than 0!")
                return redirect("add_coupon")

            # Validate max_discount
            if not max_discount.isdigit() or int(max_discount) < int(off_percent):
                messages.warning(request, "Max discount must be a number greater than or equal to Off percent!")
                return redirect("add_coupon")
            
            # Validate expiry_date
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            except ValueError:
                messages.warning(request, "Invalid expiry date format. Please use YYYY-MM-DD.")
                return redirect("add_coupon")

            if expiry_date <= timezone.now().date():
                messages.warning(request, "Expiry date should be in the future!")
                return redirect("add_coupon")

            coupon = Coupon.objects.create(
                        coupon_code = coupon_code,
                        min_amount = min_amount,
                        off_percent = off_percent,
                        max_discount = max_discount,
                        expiry_date = expiry_date_str
                    ).save()
            messages.success(request, f'{coupon_code} added successfully !')
            return render(request, "adminpanel/add_coupon.html")

        return render(request, "adminpanel/add_coupon.html")
    except:
        return render(request, 'adminpanel/error-404-admin.html')


@login_required
@user_passes_test(super_admincheck)
def edit_coupon(request, id):
    try:
        if request.method == "POST":
            coupon_code = request.POST.get("coupon_code")
            min_amount = request.POST.get("min_amount")
            off_percent = request.POST.get("off_percent")
            max_discount = request.POST.get("max_discount")
            expiry_date_str = request.POST.get("expairy_date")

            Coupon.objects.filter(id = id).update(
                coupon_code = coupon_code,
                min_amount = min_amount,
                off_percent = off_percent,
                max_discount = max_discount,
                expiry_date = expiry_date_str
            )
            messages.success(request, f'{coupon_code} updated succesfully.')
            return redirect(coupons_list)

        coupon = Coupon.objects.get(id=id)
        context = {
            'coupon': coupon
        }
        return render(request, 'adminpanel/edit_coupon.html', context)
    except:
        return render(request, 'adminpanel/error-404-admin.html')