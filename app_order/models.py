from django.db import models
from django.contrib.auth.models import User
import string
import random
from datetime import datetime
from app_accounts.models import UserAddress
from app_products.models import Product


# Create your models here.
def generate_order_id():
    """ throug this function we generate a 14 character Order ID  """
    while True:
        letters = string.ascii_uppercase + string.digits
        order_id = ''.join(random.choice(letters) for i in range(9))
        year = str(datetime.now().year)[-2:]
        month = str(datetime.now().month)[-2:]
        day = str(datetime.now().day)
        hour = str(datetime.now().hour)
        new_id = "BKST" + year + month + day + hour + order_id
        return new_id
    
class PaymentMethod(models.Model):
    method = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.method

class Payment(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount_paid = models.FloatField(null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_method.method
    

class OrderAddress(models.Model):
    fullname = models.CharField(max_length=150, null=True)
    contact_number = models.CharField(max_length=12, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house_name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.fullname


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=50, default=generate_order_id, unique=True)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True)
    order_address = models.ForeignKey(OrderAddress, on_delete=models.CASCADE, null=True, blank= True)
    order_total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    discount_amount = models.BigIntegerField(default=0)
    coupon_discount = models.BigIntegerField(default=0)

    def __str__(self):
        return self.order_id
    
class OrderItem(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='pending')

    def __str__(self):
        return self.product.product_name

    def sub_total(self):
        return self.product_price * self.quantity

    def sub_total_with_offer(self):
        return int((self.sub_total()) - (self.sub_total() * self.product.offer.off_percent) / 100)
    
    def sub_total_with_category_offer(self):
        return int((self.sub_total()) - (self.sub_total() * self.product.category.offer.off_percent)/100 )












