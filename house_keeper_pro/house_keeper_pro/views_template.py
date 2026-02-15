# common_core/views.py
from django.shortcuts import render
from house_keeper_pro.views import list_view, create_view, update_view, delete_view
from django.views.generic import TemplateView

from house_keeper_pro.utils.filters import FilterCollection
from .forms import NoteForm
from .models import Notes


MODELS_AND_FORMS = {
    'Notes': {'class': Notes, 'form': NoteForm}, 
    }

class AppsView(TemplateView):    
    template_name = 'notes_list.html'  # главная страница приложения


class NotesView(TemplateView):
    HEADERS = [
        {'note_date': 'Дата созданиия'},
        {'note_type': 'Тип'},
        {'note_category': 'Приложение'},
        {'note_text': 'Содержание заметки или размышления / формулирование задачи'},
    ]
    FILTERS = ['note_type', 'note_category']

    model_name = Notes
    model_form = NoteForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)


def prepare_filters_and_headers(model_name, FILTERS, HEADERS):
    """Подготавливает фильтры и заголовки"""
    filters_collection = FilterCollection()
    for el in FILTERS:
        filters_collection.add_filter(model_name, el)

    # filters = filters_collection.as_dict()

    headers = []
    for header in HEADERS:
        print('header: ', header)
        for key, value in header.items():
            headers.append({'field':key, 'label':value})

    return filters_collection, headers

def list_item(request, model_name, model_form, FILTERS, HEADERS):
    # Подготовка фильтров и заголовков
    filters_collection, headers = prepare_filters_and_headers(model_name, FILTERS, HEADERS)

    app_namespace = request.resolver_match.namespace
    print('app_namespace:\n', app_namespace)    

    return list_view(request, model_name, model_form, app_namespace, filters=filters_collection, headers=headers)

def add_item(request):
    model_name = request.session.get('model_name')
    print('model_name: ', model_name)
    print('MODELS_AND_FORMS', MODELS_AND_FORMS[model_name]['form'])

    return create_view(request, MODELS_AND_FORMS[model_name]['form'])

# def edit_item(request, model_name, model_form, pk):
#    model_form = request.session.get('model_form')
#    model_name = request.session.get('model_name')

#    print('model_form: ', model_form)
#    print('model_name: ', model_name)
#    return update_view(request, model_name, model_form, pk)

# def delete_item(request, model_name, pk):
#    model_name = request.session.get('model_name')
#    print('model_name: ', model_name)
#    return delete_view(request, model_name, pk)