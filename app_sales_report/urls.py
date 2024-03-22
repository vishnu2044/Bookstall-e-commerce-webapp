from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sales_report/', views.sales_report, name="sales_report"),
    path('today_report/', views.today_report, name="today_report"),
    path('week_report/', views.week_report, name="week_report"),
    path('month_report/', views.month_report, name="month_report"),
    

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
