from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_products/', views.admin_products, name='admin_products'),
    path('add_product_page/', views.add_product_page, name='add_product_page'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('unlist_product/<int:id>/', views.unlist_product, name='unlist_product'),
    path('list_product/<int:id>/', views.list_product, name='list_product'),
    path('admin_product_reviews/<int:id>/', views.admin_product_reviews, name='admin_product_reviews'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




