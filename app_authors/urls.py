from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_authors/', views.admin_authors, name = 'admin_authors'),
    path('add_author/', views.add_author, name = 'add_author'),
    path('add_author_page/', views.add_author_page, name = 'add_author_page'),
    path('edit_author/<int:id>/', views.edit_author, name = 'edit_author'),
    path('authors_page/', views.authors_page, name = 'authors_page'),
    path('author_books/<int:id>/', views.author_books, name = 'author_books'),
    path('search_authors/', views.search_authors, name = 'search_authors'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


