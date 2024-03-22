from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import razorpay
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_accounts.views import handle_login
from app_checkout.views import checkout


# Create your views here.
def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart  

# payment for cashon delivery 
def payments(request, total=0, ):
    if request.user.is_authenticated:
        payment_method = PaymentMethod.objects.get(method = "cod_method")
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
        )
        payment.save()
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.payment = payment
        order.status = 'accepted'
        order.save()
    
        # move the cart items into ordered items
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            product_price = 0
            if cart_item.product.offer and cart_item.product.offer.is_expired != True:
                product_price = cart_item.product.get_offer_price()
            elif cart_item.product.category.offer and cart_item.product.category.offer.is_expired != True:
                product_price = cart_item.product.get_offer_price_by_category()
            else:
                product_price = cart_item.product.price
            
            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                product_price = product_price,
                quantity = cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()

            total += orderitem.sub_total()


        #reduce the stock of ordered product.
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()
        discount_amount = 0

        try:
            cart = Cart.objects.get(session_id=_session_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                session_id = _session_id(request)
        )
        if cart.coupon:
            discount_amount = total * cart.coupon.off_percent / 100
            if discount_amount > cart.coupon.max_discount:
                discount_amount = cart.coupon.max_discount
            if discount_amount:
                total -= discount_amount
            

        CartItem.objects.filter(user=request.user).delete()

        # mess = f'Hello\t{request.user.first_name} {request.user.last_name} \nYour order of { product_name} has confirmed.\n Thanks!'

        # send_mail(
        #     "Thank you for your order",
        #     mess,
        #     settings.EMAIL_HOST_USER,
        #     [request.user.email],
        #     fail_silently=False,
        # )

        CartItem.objects.filter(user=request.user).delete()

        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order_item = OrderItem.objects.filter(user=request.user)

        context = {
            "total": total,
            "order": order,
            "order_items": order_item,
        }
        

        return render(request, 'temp_home/confirm.html', context)

    else:
        messages.error(request, 'You need to login first')
        return redirect(handle_login)
    

def place_order(request):
    if request.user.is_authenticated:
        current_user = request.user
        total = 0
        cart_items = CartItem.objects.filter(user = current_user)
        cart_count = cart_items.count()
        og_total = 0
        off_percent = None
        discount_amnt = 0
        coupon_discount = 0
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                print("cart item out of stock")
                return redirect('cart')
            og_total += cart_item.sub_total()
            
            if cart_item.product.offer and cart_item.product.offer.is_expired != True:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.category.offer and cart_item.product.category.offer.is_expired != True:
                total += cart_item.sub_total_with_category_offer()
            else:
                total += cart_item.sub_total()

            coupon_discount = cart_item.coupon_discount
        offer_discount = og_total - total
        total -= discount_amnt
        try:
            cart = Cart.objects.get(session_id=_session_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                session_id = _session_id(request)
        )

        if cart.coupon:
            discount_amount = total * cart.coupon.off_percent / 100

            if discount_amount > cart.coupon.max_discount:
                discount_amount = cart.coupon.max_discount
                
            if discount_amount:
                total -= discount_amount

            
        if cart_count <= 0:
            return redirect('home')

        if request.method == "POST":
            addr = request.POST["address"]
            address = UserAddress.objects.get(id=addr)
        else:
            address = UserAddress.objects.filter(user=current_user).first()

        order_address = OrderAddress.objects.create(
            fullname = address.fullname,
            contact_number = address.contact_number,
            user = address.user,
            house_name = address.house_name,
            landmark = address.landmark,
            city = address.city,
            district = address.district,
            state = address.state,
            country = address.country,
            pincode = address.pincode

        )
        order_address.save()

        data = Order()
        data.user = current_user
        data.order_address = order_address
        data.address = address
        data.order_total = total

        data.save()
        order = Order.objects.get(user = current_user, 
                                  status = data.status, 
                                  order_id = data.order_id, 
                                  order_total = data.order_total
                                )

        client = razorpay.Client(auth=( settings.KEY_ID, settings.KEY_SECRET ))
        payment = client.order.create({"amount" : total * 100, 'currency': "INR", "payment_capture" : 1})

        context = {
            'discount_amnt' : discount_amnt,
            'cart' : cart,
            'total' : total,
            'og_total' : og_total,
            'order' : order,
            'cart_items' : cart_items,
            "payment" : payment,
        }
        return render(request, 'temp_home/payments.html', context)
    else:
        messages.error(request, 'you need to login first')
        return redirect(handle_login)


def payment_success(request, total=0):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        payment_method = PaymentMethod.objects.get(method = "raz_method")
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
            amount_paid = order.order_total,
            status = 'paid'
        )
        payment.save()
        
        order.payment = payment
        order.status = 'accepted'
        order.save()
        cart_items = CartItem.objects.filter(user = request.user)

        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            product_price = 0
            if cart_item.product.offer and cart_item.product.offer.is_expired != True:
                product_price = cart_item.product.get_offer_price()
            elif cart_item.product.category.offer and cart_item.product.category.offer.is_expired != True:
                product_price = cart_item.product.get_offer_price_by_category()
            else:
                product_price = cart_item.product.price
            print("****************", product_price, "***********************")
            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                product_price = product_price,
                quantity = cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()
            total += cart_item.sub_total()

        #reduce the stock of ordered product.
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()


        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order_item = OrderItem.objects.filter(user=request.user)
        CartItem.objects.filter(user=request.user).delete()

        context = {
            "order": order,
            "order_items": order_item,
        }
            
  
        return render(request, 'temp_home/confirm.html', context)
    else:
        messages.error(request, 'you need to login first')
        return redirect(handle_login)




def add_user_address(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            name = request.POST.get("name")
            ph_no = request.POST.get("number")
            house = request.POST.get("house")
            landmark = request.POST.get("landmark")
            district = request.POST.get("district")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            pincode = request.POST.get("pincode")

                        
            if len(name) == 0:
                messages.warning(request, 'please enter name')
                return redirect(checkout)
            
            if len(ph_no) == 0:
                messages.warning(request, 'please enter phone number')
                return redirect(checkout)
            
            if len(ph_no) > 10:
                messages.warning(request, 'Phone number length must be minimum 10')
                return redirect(checkout)
            
            if len(name) == 0:
                messages.warning(request, 'please enter house name')
                return redirect(checkout)
            
            if len(landmark) == 0:
                messages.warning(request, 'please enter your landmark')
                return redirect(checkout)
            
            if len(district) == 0:
                messages.warning(request, 'please enter your district')
                return redirect(checkout)
            
            if len(city) == 0:
                messages.warning(request, 'please enter your city')
                return redirect(checkout)
            
            if len(state) == 0:
                messages.warning(request, 'please enter your sate')
                return redirect(checkout)
            
            if len(country) == 0:
                messages.warning(request, 'please enter your country')
                return redirect(checkout)
            
            if len(pincode) == 0:
                messages.warning(request, 'please enter your pincode')
                return redirect(checkout)

            
            UserAddress.objects.create(
                fullname = name,
                contact_number = ph_no,    
                user = request.user,
                house_name = house,
                landmark = landmark,
                city = city,
                district = district,
                state = state,
                country = country,
                pincode = pincode,
            ).save()
            return redirect('place_order')
    else:
        messages.error(request, 'you need to login to access this page')
        return redirect(handle_login)


def user_order_list(request):
    if request.user.is_authenticated:

        order_items = OrderItem.objects.filter(user = request.user).order_by('-id')

        per_page = 5
        page_number = request.GET.get('page')
        paginator = Paginator(order_items, per_page)

        try:
            current_page = paginator.page(page_number)

        except PageNotAnInteger:
            current_page = paginator.page(1)

        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context  ={
            "current_page" : current_page,
        } 
        return render(request, 'temp_home/user_order_list.html', context)
    
    else:
        messages.error(request, 'you need to login to access this page')
        return redirect(handle_login)        


def user_order_cancel(request, id):
    if request.user.is_authenticated:
        order_item = OrderItem.objects.get(id=id)
        if order_item.status == "accepted":
            order_item.status = "Cancelled"
            order_item.save()
        return redirect(user_order_list )
    else:
        messages.error(request, 'you need to login to access this page')
        return redirect(handle_login) 


def user_order_detail(request, id):
    if request.user.is_authenticated:
        order_item = OrderItem.objects.get(id=id)
        context = {
            'order_item': order_item
        }
        return render(request, 'temp_home/order_item_details.html', context)
    else:
        messages.error(request, 'you need to login to access this page')
        return redirect(handle_login) 


def order_invoice(request, id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id, user = request.user)
        order_items = OrderItem.objects.filter(order=order)

        for order_item in order_items:
            order_item.total_price = order_item.product.price * order_item.quantity

        total_discount = order.discount_amount + order.coupon_discount

        context = {
            "total_discount": total_discount,
            "order": order,
            "order_items": order_items,
        }
        return render(request, 'order_invoice.html', context)
    
    else:
        messages.error(request, 'you need to login to access this page')
        return redirect(handle_login) 
