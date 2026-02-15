from django.urls import path
from . import views

app_name = 'house_keeper_hub'

urlpatterns = [
    path('', views.hub_view, name='hub'),  # Главная страница
]