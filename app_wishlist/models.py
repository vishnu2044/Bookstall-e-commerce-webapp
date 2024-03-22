from django.db import models
from django.contrib.auth.models import User
from app_products.models import *

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.product_name