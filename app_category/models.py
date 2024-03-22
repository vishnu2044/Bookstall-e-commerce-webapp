from django.db import models
from app_offer.models import Offer


# Create your models here.
class Category_list(models.Model):
    category_name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True, blank= True)
    category_description = models.TextField()
    is_available = models.BooleanField(default=False)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
