from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from app_order.models import *
from app_products.models import *
from app_authors.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth
from django.db.models import F
from django.db.models import Sum
import calendar
from django.db.models import Count
# Create your views here.
#<<<<<<<<<<<<<<<<<<<<   checks if the user is authenticated and super user  >>>>>>>>>>>>>>>>>>>>
def super_admincheck(user):
    if user.is_authenticated and user.is_superuser:
        return True
    return False



#<<<<<<<<<<<<<<<<<<<<   redirect to the admin dashboard  >>>>>>>>>>>>>>>>>>>>
def get_month_name(month_number):
    if 1 <= month_number <= 12:
        return calendar.month_name[month_number]
    else:
        return None


def admin_dashboard(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            print("admin panel working>>>>>>>>>>>>>>>>>>>")

        
            order_count = OrderItem.objects.count()
            # order_count = delivered_item.count()
            product_count = Product.objects.count()
            author_count = Authors.objects.count()
            category_count = Category_list.objects.count()
            user_count = User.objects.count()                                                                                             

            #<<<<<<<<<< order status >>>>>>>>>>>
            pending_count = OrderItem.objects.filter(status__iexact="pending").count()
            accepted_count = OrderItem.objects.filter(status__iexact="accepted").count()
            shipped_count = OrderItem.objects.filter(status__iexact="shipped").count()
            delivered_count = OrderItem.objects.filter(status__iexact="delivered").count()
            cancelled_count = OrderItem.objects.filter(status__iexact="cancelled").count()
            refunded_count = OrderItem.objects.filter(status__iexact="refunded").count()

            # Calculating revenue
            
            # filtering the delivered items from the OrderItem
            delivered_items = OrderItem.objects.filter(status__iexact="delivered")

            # sales report by month for the graph
            today = timezone.now().date()
            five_months_ago = today - timedelta(days=150)
            sales_report = (
                OrderItem.objects.annotate(month=TruncMonth('created_at'))
                .filter(created_at__gte= five_months_ago, status__iexact="delivered")
                .values(month = F('month__month'))
                .annotate(total_sales= Sum('product_price'), total_number_orders = Sum('quantity'))
                .order_by('month')
            )
            for entry in sales_report:
                entry['month_name'] = get_month_name(entry['month'])

            revenue = 0
            for item in delivered_items:
                revenue += (item.product_price * item.quantity )

            raz_total = 0
            try:
                raz_method = PaymentMethod.objects.get(method = 'raz_method')  # Use get() to retrieve the specific payment method
                raz_orders = Order.objects.filter(payment__payment_method=raz_method)  # Double underscore to navigate to related fields
                razorpay_items = delivered_items.filter(order__in=raz_orders)
                for item in razorpay_items:
                    raz_total += (item.product_price * item.quantity)
            except PaymentMethod.DoesNotExist:
                print("payment does not excists>>>>>>>>>>>>>>>>>>>>>>>>")
    # Double underscore to navigate to related fields


            ## Through cod  ##
            cod_total = 0
            try:
                cod_method = PaymentMethod.objects.get(method = 'cod_method')  
                cod_orders = Order.objects.filter(payment__payment_method=cod_method)  
                cod_items = delivered_items.filter(order__in=cod_orders)  

                for item in cod_items:
                    cod_total += item.product_price * item.quantity
            except PaymentMethod.DoesNotExist:
                print("paytment method does not excists!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            
            # latest orders
            order_items = OrderItem.objects.all().order_by('-id')[:5]

            context = {
                "order_items" : order_items[:5],
                'order_count' : order_count,
                'product_count' : product_count,
                'author_count' : author_count,
                'category_count' : category_count,
                'user_count' : user_count,
                #order status
                'pending_count' : pending_count,
                'accepted_count' : accepted_count,
                'shipped_count' : shipped_count,
                'delivered_count' : delivered_count,
                'cancelled_count' : cancelled_count,
                'refunded_count' : refunded_count,

                #revenue count
                'revenue' : revenue,
                'raz_total' : raz_total,
                'cod_total' : cod_total,


                'sales_report' : sales_report,  
            }
            print(context)
            
            return render(request, 'adminpanel/ad_dashboard.html', context)
        messages.error(request, 'Only admin can access this page !')
        return render(request, 'adminpanel/admin_login.html')
    except:
        messages.warning(request, 'Oops somwthing went wrong!')
        return redirect(admin_dashboard)

#<<<<<<<<<<<<<<<<<<<<   admin login function  >>>>>>>>>>>>>>>>>>>>
def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')

        if not username.strip():
            messages.error(request, 'Please enter username.')
            return redirect(adminlogin)

        if not password.strip():
            messages.error(request, 'Please enter password.')
            return redirect(adminlogin)

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, f' {username} logined succesfully ')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid superuser credentials')
            return redirect(adminlogin)

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin_dashboard)

    return render(request, 'adminpanel/admin_login.html')



#<<<<<<<<<<<<<<<<<<<<   admin logout function  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_logout(request):
    logout(request)
    return redirect(adminlogin)


#<<<<<<<<<<<<<<<<<<<<  user details page to get all user detail   >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def user_details(request):
    user = User.objects.all()

    return render(request, 'adminpanel/user.html', {'users':user})


#<<<<<<<<<<<<<<<<<<<<  to block a user in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def block_user(request, id):
    user = User.objects.get(id=id)
    name = user.first_name
    user.is_active = False
    user.save()
    messages.success(request, f'User " {name} " is blocked')
    return redirect(user_details)


#<<<<<<<<<<<<<<<<<<<<  to unblock a user in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)   
def unblock_user(request, id):
    user = User.objects.get(id=id)
    name = user.first_name
    user.is_active = True
    user.save()
    messages.success(request, f'User " {name} " is unblocked')
    return redirect(user_details)





def error_404(request):
    return render(request, 'adminpanel/error-404-admin.html')