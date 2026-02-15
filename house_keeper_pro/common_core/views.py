# common_core/views.py
from django.db.models import Model
from django.shortcuts import render
from house_keeper_pro.views import list_view, create_view, update_view, delete_view
from django.views.generic import TemplateView

from house_keeper_pro.utils.filters import FilterCollection
from .forms import AppsForm, ActionsForm, QAForm, ActivesForm, OrgForm, NoteForm, CatForm, SubCatForm, BookForm, PlanForm, PeriodsForm, FamilyUsersForm, ActsCategoriesForm, ActSubCategoriesForm
from .models import KeeperApps, Actions, QueryAnswers, Actives, Organizations, Notes, Categories, SubCategories, Books, Plans, Periods, FamilyUsers, ActsCategories, ActSubCategories


MODELS_AND_FORMS = {
    'KeeperApps': {'class': KeeperApps, 'form': AppsForm},
    'FamilyUsers': {'class': FamilyUsers, 'form': FamilyUsersForm},
    'ActsCategories': {'class': ActsCategories, 'form': ActsCategoriesForm},
    'ActSubCategories': {'class': ActSubCategories, 'form': ActSubCategoriesForm},
    'Actions': {'class': Actions, 'form': ActionsForm},
    'Periods': {'class': Periods, 'form': PeriodsForm},
    'QueryAnswers': {'class': QueryAnswers, 'form': QAForm},
    'Notes': {'class': Notes, 'form': NoteForm},
    'Categories': {'class': Categories, 'form': CatForm},
    'SubCategories': {'class': SubCategories, 'form': SubCatForm},
    'Books': {'class': Books, 'form': BookForm},
    'Plans': {'class': Plans, 'form': PlanForm},
    'Actives': {'class': Actives, 'form': ActivesForm},
    'Organizations': {'class': Organizations, 'form': OrgForm},
    }

class CommonCoreView(TemplateView):    
    template_name = 'notes_list.html'  # главная страница

class AppsView(TemplateView):
    HEADERS = [
        {'appname': 'Приложение'},
        {'applabel': 'Наименование'},
    ]
    FILTERS = []

    model_name = KeeperApps
    model_form = AppsForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class ActsCategoriesView(TemplateView):
    HEADERS = [
        {'actscategory': 'Категория действия'},        
    ]
    FILTERS = []

    model_name = ActsCategories
    model_form = ActsCategoriesForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class ActSubCategoriesView(TemplateView):
    HEADERS = [
        {'actsubcategory': 'Действие'},
        {'actscategory': 'Приложение'},
        {'actstatus': 'Статус'},
        {'addactdate': 'Дата добавления'},
        
    ]
    FILTERS = []

    model_name = ActSubCategories
    model_form = ActSubCategoriesForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class ActionsView(TemplateView):
    HEADERS = [
        {'action': 'Действие'},
        {'keeperapps': 'Приложение'},
        {'actionprd': 'Периодичность'},
        
    ]
    FILTERS = []

    model_name = Actions
    model_form = ActionsForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class FamilyUsersView(TemplateView):
    HEADERS = [
        {'username': 'Имя пользователя'},
        {'usernick': 'Ник пользователя'},        
    ]
    FILTERS = []

    model_name = FamilyUsers
    model_form = FamilyUsersForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)


class PeriodsView(TemplateView):
    HEADERS = [
        {'prdname': 'Периодичность'}        
    ]
    FILTERS = []

    model_name = Periods
    model_form = PeriodsForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class QAView(TemplateView):
    HEADERS = [
        {'shortquery': 'Формулировка'},
        {'appsname': 'Приложение'},
        # {'querykind': 'Тип'},
        {'asktime': 'Время'},
        {'status': 'Статус'}
    ]
    FILTERS = ['appsname', 'status']

    model_name = QueryAnswers
    model_form = QAForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

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

class CategoriesView(TemplateView):
    HEADERS = [
        {'catname': 'Наименование'},
        {'catbuhtype': 'Доход/расход'},
        {'catusertype': 'Вид категории'},
        {'catstatus': 'Статус категории'},
        {'catperiod': 'Периодичность категории'},
        
    ]
    FILTERS = ['catbuhtype', 'catstatus', 'catperiod']

    model_name = Categories
    model_form = CatForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class SubCategoriesView(TemplateView):
    HEADERS = [
        {'prodname': 'Наименование'},
        {'prodcategory': 'Категория'},
        {'prodbasket': 'Корзина/набор'},
        {'prodcoment': 'Описание/применение'},
        {'is_nesessary': 'Наличие'},
    ]
    FILTERS = ['prodcategory', 'prodbasket', 'is_nesessary']

    model_name = SubCategories
    model_form = SubCatForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)

class BooksView(TemplateView):
    HEADERS = [
        {'book_name':'Название книги'},
        {'author':'Автор'},
        {'tag_name': 'Область/тэг'},
        {'bookcost':'Стоимость'},
        {'publ_year':'Год издания'},
        {'is_verified':'В наличии'}        
    ]

    FILTERS = ['tag_name', 'publ_year']

    AGG_FIELD = {'agg_field':'bookcost', 'agg_label': 'На сумму', 'count_label': 'книг'}

    model_name = Books
    model_form = BookForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS, self.AGG_FIELD)

class PlansView(TemplateView):
    HEADERS = [
        {'nameplan': 'Наименование плана'},
        {'plan_type': 'Приложение'},
        {'start_date': 'Дата начала'},
        {'finish_date': 'Дата окончания'},
        {'create_date': 'Дата создания'}
    ]
    FILTERS = ['plan_type', 'create_date']    

    model_name = Plans
    model_form = PlanForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name,  self.model_form, self.FILTERS, self.HEADERS)


class ActivesView(TemplateView):
    HEADERS = [
        {'account_num': 'Номер счета'},
        {'account_finorg': 'Финансовая организация'},
        {'account_country': 'Юрисдикция'},
        {'account_type': 'Тип'},
        # {'account_owner': 'Владелец'},
        {'owner_name': 'Имя владельца'},        
        {'account_opendate': 'Дата открытия'},
        {'account_coment': 'Доп информация'},
        {'account_sum': 'Текущая сумма'},
    ]
    FILTERS = ['account_finorg', 'account_type', 'owner_name']

    AGG_FIELD = {'agg_field':'account_sum', 'agg_label': 'Капитал', 'count_label': 'счетов'}

    model_name = Actives
    model_form = ActivesForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name, self.model_form, self.FILTERS, self.HEADERS, self.AGG_FIELD)

class OrganisationsView(TemplateView):
    HEADERS = [
        {'org_name': 'Наименование организации'},
        {'org_type': 'Тип организации'},
        {'org_legal': 'Юрисдикция организации'},
    ]
    FILTERS = ['org_type', 'org_legal']

    model_name = Organizations
    model_form = OrgForm
    template_name = 'general_list.html'

    def get(self, request):
        return list_item(request, self.model_name, self.model_form, self.FILTERS, self.HEADERS)


def prepare_filters_and_headers(model_class, FILTERS, HEADERS):
    """Подготавливает фильтры и заголовки"""
    filters_collection = FilterCollection()
    for el in FILTERS:
        filters_collection.add_filter(model_class, el)

    headers = []
    for header in HEADERS:
        print('header: ', header)
        for key, value in header.items():
            headers.append({'field':key, 'label':value})

    return filters_collection, headers

def list_item(request, model_class=None, model_form=None, FILTERS=None, HEADERS=None, AGG_FIELD=None):
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

    return list_view(request, model_class, model_form, app_namespace, filters=filters_collection, headers=headers, agg_field=AGG_FIELD)

def add_item(request):
    # Получаем данные из сессии, сохранённые в предыдущем представлении
    # shared_context = request.session.get('shared_context', {})
    # model_form = shared_context.get('model_form')  # Или другое нужное вам значение
    # print('add_item: ', request)
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