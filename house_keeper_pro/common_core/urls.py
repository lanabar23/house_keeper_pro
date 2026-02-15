from django.contrib import admin
from django.urls import path
from . import views

app_name = 'commoncore'

urlpatterns = [
    path('', views.CommonCoreView.as_view(), name='common_core'), 
    path('apps/', views.AppsView.as_view(), name='apps'),
    path('users/', views.FamilyUsersView.as_view(), name='users'),
    path('actscategories/', views.ActsCategoriesView.as_view(), name='actscategories'),
    path('actsubcategories/', views.ActSubCategoriesView.as_view(), name='actsubcategories'),
    path('actions/', views.ActionsView.as_view(), name='actions'),
    path('periods/', views.PeriodsView.as_view(), name='periods'),
    path('qa/', views.QAView.as_view(), name='qa'),
    path('notes/', views.NotesView.as_view(), name='notes'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('subcategories/', views.SubCategoriesView.as_view(), name='subcategories'),
    path('plans/', views.PlansView.as_view(), name='plans'),
    path('actives/', views.ActivesView.as_view(), name='actives'),
    path('organizations/', views.OrganisationsView.as_view(), name='orgs'),
    path('root/', views.list_item, name='root'),
    path('list/', views.list_item, name='list'),
    path('add/', views.add_item, name='add'),
    path('edit/', views.edit_item, name='edit'),
    # path('delete/<int:pk>/', views.delete_item, name='delete'),
    # path('tasks/', views.TasksListView.as_view(), name='tasks_list'),  <int:pk>/
    # path('notes/', views.NotesListView.as_view(), name='notes_list'),
    # path('refbooks/', views.RefBooksListView.as_view(), name='refbooks_list'),
    # path('add_item/', views.add_item, name='add_item'),
    # path('edit_item/<int:pk>/', views.edit_item, name='edit_item'),
    # path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    # path('search_item/', views.search_item, name='search_item'),
]

