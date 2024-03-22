from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_order_list/', views.admin_order_list, name = 'admin_order_list'),
    path('update_order_status/<int:id>/', views.update_order_status, name = 'update_order_status'),
    path('order_details/<int:id>/', views.order_details, name = 'order_details'),
    path('search_orders/', views.search_orders, name = 'search_orders'),



 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


