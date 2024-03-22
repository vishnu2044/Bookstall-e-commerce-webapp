from django.shortcuts import render, redirect
from app_order.models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin_panel.views import super_admincheck
from app_order.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


# Create your views here.

#<<<<<<<<<<<<<<<<<<<<  To display order list in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_order_list(request):
    try:
        order_items = OrderItem.objects.all().order_by('-id')


        per_page = 10
        page_number = request.GET.get('page')
        paginator = Paginator(order_items, per_page) 

        try:
            current_page = paginator.page(page_number)

        except PageNotAnInteger:
            current_page = paginator.page(1)

        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context = {
            "current_page" : current_page,
            "order_items" : order_items
        }
        return render(request, 'adminpanel/order_list.html', context)
    
    except:
        return render(request, 'adminpanel/error-404-admin.html')


#<<<<<<<<<<<<<<<<<<<<  To update order order status in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def update_order_status(request, id):
    try:
        order_item = OrderItem.objects.get(id=id)
        if request.method == "POST":
            status = request.POST["status"]
            order_item.status = status
            order_item.save()

            try:
                order = OrderItem.order
                payment_method = PaymentMethod.objects.get(method = 'cod_method')
                if (order_item.status == "delivered" or order_item.status == "Delivered") and order.payment.status != "paid":
                    payment = Payment(
                        user = request.user,
                        payment_method = payment_method,
                        amount_paid = order.order_total,
                        status = 'paid'
                    )
                    payment.save()
            except:
                pass

            current_user = order_item.user
            subject = f'{order_item} {order_item.status}'
            mess = f"Hello\t{current_user.first_name}.\nYour {order_item} has been {order_item.status}, Track your order in our website.\nThank You!"
            send_mail(
                    subject,
                    mess,
                    settings.EMAIL_HOST_USER,
                    [current_user.email],
                    fail_silently= False
                )
            messages.success(request, "status updates successfully!")
            return redirect(order_details, id )

    except OrderItem.DoesNotExist:
        messages.error(request, "oops something wrong!")
        
    context = {"id":id}
    return render(order_details, context )


@login_required
@user_passes_test(super_admincheck)
def order_details(request, id):
    try:
        order_item = OrderItem.objects.get(id=id)
        context = {
            "order_item" : order_item,
            "id" : id
        }
        return render(request, 'adminpanel/order_details.html', context)
    

    except OrderItem.DoesNotExist:
        messages.error(request, "oops something wrong!")
        
    order_item = OrderItem.objects.get(id=id)
    context = {
            "order_item" : order_item,
            "id" : id
        }
    return render(order_details, context )


@login_required
@user_passes_test(super_admincheck)
def search_orders(request):
    try:
        search_text = request.POST.get("query")

        product = Product.objects.filter(product_name__icontains = search_text)

        order_id = Order.objects.filter(order_id__icontains = search_text)

        username = User.objects.filter(username__icontains = search_text)

        combined_query = Q()
        combined_query |= Q(product_id__in=product.values_list('id', flat=True))
        combined_query |= Q(order_id__in=order_id.values_list('id', flat=True))
        combined_query |= Q(user_id__in=username.values_list('id', flat=True))

        order_items = OrderItem.objects.filter(combined_query)

        per_page = 10
        page_number = request.GET.get('page')
        paginator = Paginator(order_items, per_page) 

        try:
            current_page = paginator.page(page_number)

        except PageNotAnInteger:
            current_page = paginator.page(1)

        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context = {
            "current_page" : order_items,
            "order_items" : order_items
        }
        return render(request, 'adminpanel/order_list.html', context)
        
    except:
        messages.error(request, "oops something wrong!")
        return render(admin_order_list)



