from django.shortcuts import render, redirect
from django.contrib import messages
from app_order.models import *
from app_products.models import *
from app_authors.models import *
from datetime import timedelta
from app_admin_panel.views import *
from datetime import date


# Create your views here.
#sales calculation 
def sales_calculation(request, start_date, end_date):
    if request.user.is_authenticated and request.user.is_superuser:

        if start_date == end_date:
            date_obj = datetime.strftime(start_date, '%Y-%m-%d')
                        
            order_items = OrderItem.objects.filter(order__created_at__date = date_obj)
        else:
            order_items = OrderItem.objects.filter(order__created_at__gte = start_date, order__created_at__lte = end_date)

        if order_items:
            order_count = order_items.distinct('order').count()
            order_item_count = order_items.count()

            # <<<<<<<<<< payement methods >>>>>>>>>>>
            delivered_items = order_items.filter(status__iexact="delivered")
            delivered_items_count = order_items.filter(status__iexact="delivered").count()

            #total revenue
            product_price_sum = 0
            for item in delivered_items:
                product_price_sum += (item.product_price * item.quantity)
            #Through razor pay
            raz_total = 0
            raz_method = PaymentMethod.objects.get(method = "raz_method")  
            raz_orders = Order.objects.filter(payment__payment_method=raz_method)
            razorpay_items = delivered_items.filter(order__in=raz_orders)

            for item in razorpay_items:
                raz_total += (item.product_price * item.quantity)

            ## Through cod  ##
            cod_total = 0
            cod_method = PaymentMethod.objects.get(method = "cod_method")  
            cod_orders = Order.objects.filter(payment__payment_method=cod_method)  
            cod_items = delivered_items.filter(order__in=cod_orders)  

            for item in cod_items:
                cod_total += ( item.product_price * item.quantity)

            calculation  ={
                'delivered_items_count' : delivered_items_count,
                'order_item_count' : order_item_count,
                'product_price_sum' : product_price_sum,
                'order_count' : order_count,
                'raz_total' : raz_total,
                'cod_total' : cod_total,

            }
            return calculation
    else:
        messages.error(request, 'Only admin can access this page !')
        return render(request, 'adminpanel/admin_login.html')     


def sales_report(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if not request.user.is_superuser:
            return redirect(admin_dashboard)
        
        context = {}
        s_date = None
        e_date = None
        start_date = None
        end_date = None
        if request.method == "POST":
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")

            if start_date == "" :
                messages.error(request, 'start date not entered')
                return redirect(sales_report)
            if end_date == "" :
                messages.error(request, 'end date not entered')
                return redirect(sales_report)
            
            if start_date == end_date:
                messages.warning(request, 'Please select a start date and end date must be deferent!')
                return redirect(sales_report)
            
            order_items = OrderItem.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)
                
            if order_items:
                context.update(sales = order_items, s_date = start_date, e_date = end_date)
                context.update(sales_calculation(request, start_date = start_date, end_date = end_date))

                messages.success(request, f'Here is the sales report covering the period from {start_date} to {end_date}.')
            else:
                messages.error(request, 'No data found at the specific date!')
        

        return render(request, 'adminpanel/sales.html', context)
    else:
        messages.error(request, 'Only admin can access this page !')
        return render(request, 'adminpanel/admin_login.html')  



def today_report(request):
    if request.user.is_authenticated and request.user.is_superuser:

        context = {}
        today = date.today()
        
        date_obj = today.strftime("%Y-%m-%d")
        order_items = OrderItem.objects.filter(order__created_at__date = date_obj)

        if order_items:
            context.update(sales = order_items, s_date=today, e_date=today)
            messages.success(request, f'Here is the sales report as of {date_obj}. ')
            context.update(sales_calculation(request, start_date = today, end_date = today))

            return render(request, 'adminpanel/sales.html' ,context)
        else:
            messages.error(request, 'no data found.')
            return render(request, 'adminpanel/sales.html')
        
    else:
        messages.error(request, 'Only admin can access this page !')
        return render(request, 'adminpanel/admin_login.html')  


def week_report(request):
    if request.user.is_authenticated and request.user.is_superuser:

        context = {}
        today = date.today()
        week = today - timedelta(days=7)

        order_items = OrderItem.objects.filter(order__created_at__gte = week, order__created_at__lte = today)
        print("************************************", order_items)
        if order_items is None:
            messages.warning(request, 'dfssssssssssssssssssssssssss')
            return render(request, 'adminpanel/sales.html')

        if order_items:
            context.update(sales = order_items, s_date = today, e_date = week)
            context.update(sales_calculation(request, start_date=week, end_date=today))
            messages.success(request, f'Here is the sales report as of last week')
            return render(request, 'adminpanel/sales.html' ,context)
        
        else:
            messages.error(request, 'no data found in the last week.')
            return render(request, 'adminpanel/sales.html')
    else:
        messages.error(request, 'Only admin can access this page !')
        return render(request, 'adminpanel/admin_login.html')  




def month_report(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        today = date.today()
        month = today - timedelta(days=30)

        order_items = OrderItem.objects.filter(order__created_at__gte = month, order__created_at__lte = today)

        if order_items:
            context.update(sales = order_items, s_date = today, e_date = month)
            context.update(sales_calculation(request, start_date = month, end_date = today))
            messages.success(request, 'Here is the sales report of last month')
            return render(request, 'adminpanel/sales.html', context)
        
        else:
            messages.error(request, 'no data found')
            return render(request, 'adminpanel/sales.html')
    else:
        messages.error(request, 'Only admin can access this page !')
        return render(request, 'adminpanel/admin_login.html')  

