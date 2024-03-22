from django.db import models
import random
from django.contrib.auth.models import User
from app_products.models import Product
from app_offer.models import Coupon 


# Create your models here.
def generate_cart_id():
    new_id = random.randint(10000000, 99999999)
    if not Cart.objects.filter(cart_id = new_id).exists():
        return new_id

class Cart(models.Model):
    cart_id = models.IntegerField(unique=True, default=generate_cart_id )
    session_id = models.TextField(default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.cart_id)
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.FloatField()
    is_acitve = models.BooleanField(default=True)  
    coupon_discount = models.FloatField(null=True, blank=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.product_name
    
    def sub_total_with_offer(self):
        return int((self.sub_total()) - (self.sub_total() * self.product.offer.off_percent) / 100)
    
    def sub_total_with_category_offer(self):
        return int((self.sub_total()) - (self.sub_total() * self.product.category.offer.off_percent)/100 )
    
