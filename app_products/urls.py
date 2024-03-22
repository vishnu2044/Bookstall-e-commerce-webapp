from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user_product_review/<int:product_id>/', views.user_product_review, name="user_product_review"),

    
]
