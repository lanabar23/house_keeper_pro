# project/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils.functional import lazy
from django.db.models.query import QuerySet
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.urls import reverse, NoReverseMatch
from .utils.filters import FilterCollection
from logging import getLogger


logger = getLogger(__name__)

def log_route(request, message):
    """Логирует маршрут и сообщение."""
    logger.info(f"[Route]: {request.path} | Message: {message}")


def generate_urls(request, app_namespace, model_class, model_form):
    """
    Генерирует URL для стандартных операций CRUD.
    """
    try:
        # Логируем попытку сформировать URL
        log_route(request, f"Формирование URL для пространства '{app_namespace}' и модели '{model_class.__name__}'.")
        
        urls = {
            # 'root': reverse(f"{app_namespace}:root"),
            'list': reverse(f"{app_namespace}:list"),
            f'add': reverse(f"{app_namespace}:add"),
            'edit': reverse(f"{app_namespace}:edit"),
            # 'delete': reverse(f"{app_namespace}:delete")
        }
        print('urls: ', urls)
        # Проверка результатов
        log_route(request, f"Успешно сформированы URL: {urls}.")
        return urls
    except (NoReverseMatch, ImproperlyConfigured) as e:
        # Логируем ошибку
        log_route(request, f"Ошибка при формировании URL: {str(e)}.")
        raise

def convert_filters_to_dict(filters_collection, request):
    """
    Преобразует коллекцию фильтров (FilterCollection) в словарь,
    подходящий для дальнейшего использования в ORM-фильтрах.
    """
    result = {}
    for item in filters_collection:
        if item.type == 'select':
            # Берём значение из GET-запроса, иначе None
            selected_value = request.GET.get(item.field_name)
            result[item.field_name] = selected_value
        else:
            # Остальные поля воспринимаются как введённые пользователем
            result[item.field_name] = request.GET.get(item.field_name)
    print('result_filters: ', result)
    return result

def apply_filters__(queryset, filters):    
    """Применяет фильтры к QuerySet."""
    print('filters:', filters)
    try:
        for filter in filters:
            for field_name, field_value in filter:
                print('filter_item:', field_name, field_value)
                if isinstance(field_value, tuple):
                    queryset = queryset.filter(**{f"{field_name}__in": field_value})
                elif field_value is not None:
                    queryset = queryset.filter(**{field_name: field_value})
        return queryset
    except Exception as e:
        error_message = 'apply_filters'
        print('Error: ', e)
        return queryset # render(request, 'error.html', {'message': error_message}, status=500)

def apply_filters(queryset, filters, request):
    """Применяет фильтры к QuerySet."""
    try:
        for filter_pair in filters:
            field_name, filter_field = filter_pair  # Развертываем кортеж в поле и объект FilterField
            
            # Извлекаем выбранное значение фильтра
            selected_value = request.GET.get(filter_field.field_name)
            
            # Формируем условие фильтрации исходя из типа поля
            if filter_field.type == 'select':
                # Если тип select, используем точное совпадение
                if selected_value is not None:
                    queryset = queryset.filter(**{field_name: selected_value})
            else:
                # Для остальных типов можем предполагать ввод текста или другое поведение
                pass  # Здесь можешь расширить логику, если нужны дополнительные проверки
                
        return queryset
    except Exception as e:
        error_message = 'apply_filters'
        print('Error: ', e)
        return queryset

def convert_filters_to_dict_new(filters, request):
    """Преобразует коллекцию фильтров в словарь."""
    result = {}
    for field in filters.fields:
        value = request.GET.get(field.name, '')
        if value:
            result[field.name] = value
    return result

def apply_filters_(queryset, filters):
    """Применяет фильтры к запросу."""
    filtered_queryset = queryset.filter(**filters)
    return filtered_queryset


def list_view(request, model_class, model_form, app_namespace, filters=None, headers=None, agg_field=None, extra_context=None, template_name='general_list.html'):
    """
    Обобщённая логика вывода списка записей с поддержкой фильтров и заголовков.
    """
    # Логируем начало обработки запроса
    log_route(request, "Начало обработки общего списка.")

    queryset = model_class.objects.all()
    # print('queryset: ', queryset)

    # Преобразование коллекции фильтров в словарь
    if isinstance(filters, FilterCollection):
        print('FilterCollection: ', FilterCollection)
        # filters = filters.as_dict() # convert_filters_to_dict(filters, request)
        filters = [(filt.field_name, filt) for filt in filters]
        

    # Применение фильтров
    if filters:
       queryset = apply_filters(queryset, filters, request)

    # Сортировка
    sort_by = request.GET.get('sort')
    print('sort_by:', sort_by)
    print("GET params:", dict(request.GET))
    if sort_by:
        try:
            # Проверяем наличие указанного поля в модели
            model_fields = [f.name for f in queryset.model._meta.fields]
            if sort_by.lstrip('-') in model_fields:  # допускаем сортировку по убыванию с минусом
                queryset = queryset.order_by(sort_by)
            else:
                raise ValueError(f"Поле '{sort_by}' не найдено.")
        except Exception as e:
            print(f"Ошибка сортировки: {e}")

    # Пагинация
    per_page = 25
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Генерация URL для основных операций CRUD
    urls = generate_urls(request, app_namespace, model_class, model_form)

    # Подготовка данных для шаблона    
    items = []
    sum = 0

    for item in page_obj.object_list:
        subitem = []        
        for header in headers:
            item_data = {}
            item_data['field'] = header['field']   
            item_data['attr'] = getattr(item, header['field'])      
            subitem.append(item_data)
            if agg_field is not None and header['field'] == agg_field['agg_field']:
                sum += item_data['attr']
        items.append(subitem)

    # Формирование контекста
    context = {
        'model_table': model_class.__name__,
        'model_form': model_form.__name__,    
        # 'total_count_label': agg_field['count_label'] or None,
        'total_items': len(items),        
        'totalsum_value': sum, # sum(items['field']['account_sum']),
        'item_name': 'задач',
        'items': items, # paginator.object_list,
        'headers': headers,  # Заголовки таблицы
        'filters': filters,
        'page_obj': page_obj,
        'add_url': urls[f'add'],
        'list_url': urls['list'],
        # 'edit_url': urls['edit'],
        # 'delete_url': urls['delete']
    }

    if agg_field is not None:
        context['total_count_label'] = agg_field['count_label']
        context['totalsum_label'] = agg_field['agg_label']
    else:
        context['total_count_label'] = context['model_table']
        context['totalsum_label'] = ''


    if extra_context:
        context.update(extra_context)

    # Сохраняем контекст в сессии для последующего использования
    request.session['model_name'] = model_class.__name__
    request.session['model_form'] = model_form.__name__
    request.session['filters'] = filters
    request.session['headers'] = headers

    try:     
        # Логируем успешное завершение этапа
        log_route(request, f"Сформированы URL: {urls}.")
        # Рендеринг шаблона
        return render(request, template_name, context)
    except Exception as e:
        # Возвращаем страницу с описанием ошибки. Подробное логирование ошибки
        error_message = f"Произошла ошибка list_view: {str(e)}"
        return render(request, 'error.html', {'message': error_message}, status=500)


def create_view(request, model_form, success_url=None, template_name='add_new.html'):
    """
    Общая логика создания записи.
    """
    if request.method == 'POST':
        # Создаем экземпляр формы, передавая POST-данные
        form = model_form(request.POST)
        
        # Проверяем форму на валидность
        if form.is_valid():  # Теперь is_valid() вызываем у формы
            form.save()
            messages.success(request, 'Запись успешно создана.')
            # return redirect(success_url)
        else:
            messages.error(request, 'Возникли ошибки при создании записи.')
    else:
        # Если GET-запрос, создаем пустую форму
        form = model_form()
    
    return render(request, template_name, {'form': form})


def update_view(request, model_class, model_form, object_id, success_url=None, template_name='general_list.html'):
    """
    Общая логика обновления записи.
    """
    obj = get_object_or_404(model_class, id=object_id)
    if request.method == 'POST':
        form = model_form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = model_form(instance=obj)
    return render(request, template_name, {'form': form, 'obj': obj})

def delete_view(request, model_class, object_id, success_url=None, template_name='general_confirm_delete.html'):
    """
    Общая логика удаления записи с предварительным подтверждением.
    """
    obj = get_object_or_404(model_class, id=object_id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Запись успешно удалена.')
        return redirect(success_url)
    return render(request, template_name, {'obj': obj})
