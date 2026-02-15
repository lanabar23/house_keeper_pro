# common_core/views.py
from django.shortcuts import render
from house_keeper_pro.views import list_view, create_view, update_view, delete_view
from django.views.generic import TemplateView

from .forms import QAForm
from .models import QAItem
from house_keeper_pro.utils.filters import FilterCollection

class CommonCoreView(TemplateView):
    
    template_name = 'notes_list.html'  # главная страница


def qa_list(request):
    print('qa_request: ', type(request), request)
    # Определяем фильтры и заголовки. Заполнения коллекции фильтров
    filters_collection = FilterCollection()
    filters_collection.add_filter(QAItem, 'appsname')  # Если appsname имеет choices, они будут использованы
    filters_collection.add_filter(QAItem, 'status')    # Аналогично

    headers = [
        {'field': 'shortquery', 'label': 'Формулировка'},
        {'field': 'appsname', 'label': 'Приложение'},
        {'field': 'querykind', 'label': 'Тип'},
        {'field': 'asktime', 'label': 'Время'},
        {'field': 'status', 'label': 'Статус'}
    ]

    app_namespace = request.resolver_match.namespace
    print('app_namespace:\n', app_namespace)    

    return list_view(request, QAItem, app_namespace, filters=filters_collection, headers=headers)
    

# 1. Определение структуры фильтров


# 2. Формирование текущих значений фильтров из GET-запроса

# 3. Создание финального формата фильтров для шаблона


#def add_item(request):
#    return create_view(request, QAItem, 'myapp:list', 'myapp/add.html')

#def edit_item(request, pk):
#    return update_view(request, QAItem, QAForm, pk, 'myapp:list', 'myapp/edit.html')

#def delete_item(request, pk):
#    return delete_view(request, QAItem, pk, 'myapp:list', 'myapp/delete.html')
