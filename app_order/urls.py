from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payments/', views.payments, name="payments"),
    path('user_order_list/', views.user_order_list, name="user_order_list"),
    path('add_user_address/', views.add_user_address, name="add_user_address"),
    path('user_order_cancel/<int:id>/', views.user_order_cancel, name='user_order_cancel'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('order_invoice/<int:id>/', views.order_invoice, name='order_invoice'),
    path('user_order_detail/<int:id>/', views.user_order_detail, name='user_order_detail'),
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)