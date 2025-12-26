from django.urls import path
from .views import HomeView, LibraryListView, add_book, edit_book, delete_book, search_books

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('library/', LibraryListView.as_view(), name='library_list'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
    path('search_books/', search_books, name='search_books'),
]