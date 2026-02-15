from django.urls import path
from .views import views

app_name = 'household'  # Убедись, что здесь правильное пространство имен

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('library/', views.LibraryListView.as_view(), name='library_list'),  # Убери пространство имен из имени пути
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('search_books/', views.search_books, name='search_books'),
]
