from django.urls import path
from . import views

app_name = 'profway'

urlpatterns = [
    path('', views.ProfiWay.as_view(), name='profi_way'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
]