from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('wishlist_view/', views.wishlist_view, name = 'wishlist_view'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name = 'add_to_wishlist'),
    path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist, name = 'remove_from_wishlist'),
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


