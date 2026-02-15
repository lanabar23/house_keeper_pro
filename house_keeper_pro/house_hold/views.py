# common_core/views.py
from django.shortcuts import render
from house_keeper_pro.views import list_view, create_view, update_view, delete_view
from django.views.generic import TemplateView

from .forms import ActDoneForm, BookDoneForm, UsersActionsForm
from .models import ActionsFacts, BooksFacts, UsersActions
from house_keeper_pro.utils.filters import FilterCollection


MODELS_AND_FORMS = {
    'UsersActions': {'class': UsersActions, 'form': UsersActionsForm}, 
    'ActionsFacts': {'class': ActionsFacts, 'form': ActDoneForm}, 
    'BooksFacts': {'class': BooksFacts, 'form': BookDoneForm}, 
    }

class HomeView(TemplateView):    
    template_name = 'notes_list.html'  # главная страница

class UsersActionsView(TemplateView):
    HEADERS = [
        {'actcat': 'Категория'},
        {'actdone': 'Действие'},
        {'actstart': 'Начало'},
        {'actplandur': 'План дл-ть'},
        {'actfactdur': 'Факт дл-ть'},
        {'actcoment': 'Комментарий/описание'},
    ]
    FILTERS = ['actcat','actdone', 'actstart']

    model_name = UsersActions
    model_form = UsersActionsForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)


class DayActionsView(TemplateView):
    HEADERS = [
        {'actdone': 'Действие'},
        {'actstart': 'Начало'},
        {'actfinish': 'Окончание'},
        {'actcoment': 'Комментарий/описание'},
    ]
    FILTERS = ['actdone', 'actstart']

    model_name = ActionsFacts
    model_form = ActDoneForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class BookActsView(TemplateView):
    HEADERS = [
        {'book_name': 'Книга'},
        {'timestart': 'Время старта'},
        {'timefin': 'Время окончания'},
        {'pagestart': 'Старт (стр)'},
        {'pagefin': 'Финиш (стр)'},
        {'bookstatus': 'Статус'},
        {'basic_thoughts': 'Главные мысли автора'},
        {'coment': 'Комментарий'},
    ]
    FILTERS = ['book_name', 'bookstatus']

    model_class = BooksFacts
    model_form = BookDoneForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_class,  self.model_form, self.FILTERS, self.HEADERS)


def prepare_filters_and_headers(model_class, FILTERS, HEADERS):
    """Подготавливает фильтры и заголовки"""
    filters_collection = FilterCollection()
    for el in FILTERS:
        filters_collection.add_filter(model_class, el)

    # filters = filters_collection.as_dict()

    headers = []
    for header in HEADERS:
        print('header: ', header)
        for key, value in header.items():
            headers.append({'field':key, 'label':value})

    return filters_collection, headers

def list_item(request, model_class=None, model_form=None, FILTERS=None, HEADERS=None):
    # Подготовка фильтров и заголовков
    if FILTERS is not None  and HEADERS is not None:
        filters_collection, headers = prepare_filters_and_headers(model_class, FILTERS, HEADERS)
    else:
        filters_collection = request.session.get('filters')
        headers =  request.session.get('headers')
        model_name = request.session.get('model_name')
        model_class = MODELS_AND_FORMS[model_name]['class'] 
        model_form = MODELS_AND_FORMS[model_name]['form'] 

    app_namespace = request.resolver_match.namespace
    print('app_namespace:\n', app_namespace)    

    return list_view(request, model_class, model_form, app_namespace, filters=filters_collection, headers=headers)

def add_item(request):
    model_name = request.session.get('model_name')
    print('model_name: ', model_name)
    print('MODELS_AND_FORMS', MODELS_AND_FORMS[model_name]['form'])

    return create_view(request, MODELS_AND_FORMS[model_name]['form'])

def edit_item(request, model_name, model_form, pk):
    model_form = request.session.get('model_form')
    model_name = request.session.get('model_name')

    print('model_form: ', model_form)
    print('model_name: ', model_name)
    return update_view(request, model_name, model_form, pk)

# def delete_item(request, model_name, pk):
#    model_name = request.session.get('model_name')
#    print('model_name: ', model_name)
#    return delete_view(request, model_name, pk)





