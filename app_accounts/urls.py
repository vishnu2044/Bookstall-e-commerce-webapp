from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.handle_login, name="handle_login"),
    path('signup/', views.signup, name="signup"),
    path('otp_login/', views.otp_login, name="otp_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('add_user_address_profile/', views.add_user_address_profile, name="add_user_address_profile"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('change_user_password/', views.change_user_password, name='change_user_password'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('edit_user_address/<int:id>/', views.edit_user_address, name='edit_user_address'),
    path('delete_user_address/<int:id>/', views.delete_user_address, name='delete_user_address'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
     

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
