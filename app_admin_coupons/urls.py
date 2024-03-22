from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.coupons_list, name = 'coupons_list'),
    path('add_coupon/', views.add_coupon, name = 'add_coupon'),
    path('edit_coupon/<int:id>/', views.edit_coupon, name="edit_coupon"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


