"""
URL configuration for BookStall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from app_accounts.views import signup
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_home.urls')),
    path('app_accounts/', include('app_accounts.urls')),
    path('shop/', include('app_products.urls')),
    path('adminpanel/', include('app_admin_panel.urls')),
    path('appadminproducts/', include('app_admin_products.urls')),
    path('authors/', include('app_authors.urls')),
    path('cart/', include('app_cart.urls')),
    path('checkout/', include('app_checkout.urls')),
    path('order/', include('app_order.urls')),
    path('adminorder/', include('app_admin_order.urls')),
    path('store/', include('app_store.urls')),
    path('wishlist/', include('app_wishlist.urls')),
    path('admin_category/', include('app_admin_category.urls')),
    path('app_admin_coupons/', include('app_admin_coupons.urls')),
    path('app_admin_coupons/', include('app_offer.urls')),
    path('app_sales_report/', include('app_sales_report.urls')),



    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)





