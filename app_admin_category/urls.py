from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('category/', views.categories_list, name = 'categories_list'),
    path('addcategory/', views.add_category, name = 'add_category'),
    path('unlistcategory/<int:id>/', views.unlist_category, name = 'unlist_category'),
    path('listcategory/<int:id>/', views.list_category, name = 'list_category'),
    path('editcategory/<int:id>/', views.edit_catgory, name='edit_catgory'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




