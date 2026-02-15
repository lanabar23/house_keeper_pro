from django.contrib import admin
from django.urls import path
from . import views

app_name = 'household'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('dayactions/', views.DayActionsView.as_view(), name='dayactions'),
    path('usersactions/', views.UsersActionsView.as_view(), name='usersactions'),
    path('bookacts/', views.BookActsView.as_view(), name='bookacts'),
    path('list/', views.list_item, name='list'),
    path('add/', views.add_item, name='add'),
    path('edit/', views.edit_item, name='edit'),
    # path('delete/', views.delete_item, name='delete'),
]

