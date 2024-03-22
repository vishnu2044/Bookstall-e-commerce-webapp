from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('offers_list/', views.offers_list, name = 'offers_list'),
    path('add_offer/', views.add_offer, name = 'add_offer'),
    path('edit_offer/<int:id>/', views.edit_offer, name = 'edit_offer'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


