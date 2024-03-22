from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('user_details/', views.user_details, name="user_details"),
    path('block_user/<int:id>/', views.block_user, name="block_user"),
    path('unblock_user/<int:id>/', views.unblock_user, name="unblock_user"),
    path('error_404/', views.error_404, name="error_404"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
