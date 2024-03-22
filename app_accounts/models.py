from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    mobile = models.CharField(max_length=10,default="")
    otp = models.CharField(max_length=6,default="")


class UserAddress(models.Model):
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