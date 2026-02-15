
from django.db.models.fields import DateField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.template.defaultfilters import register
from collections import namedtuple
import decimal

FilterField = namedtuple(
    'FilterField',
    ['field_name', 'type', 'options'],
    defaults=['input', {}],  # default values for type and options
)

class FilterCollection(list):
     def add_filter(self, model_class_or_field_name, field_name=None, type='input', options=None):
        try:
            if isinstance(model_class_or_field_name, str):
                # Простое имя поля передано, применяем стандартные правила
                print('str_filed: ', field)
                super().append(FilterField(field_name, type, options))
            else:
                # Пара модель + имя поля переданы
                field = model_class_or_field_name._meta.get_field(field_name)
                if isinstance(field, ForeignKey):
                    # Если поле - это ForeignKey, используем связанный Model
                    target_model = field.remote_field.model
                    if not options:
                        # Получаем список объектов для выбора
                        choices = [(obj.pk, str(obj)) for obj in target_model.objects.all()]
                        options = dict(choices)
                    super().append(FilterField(field_name, 'select', options))
               
                # Особый случай обработки полей типа Дата и Время
                elif isinstance(field, (DateField, DateTimeField)):
                    print('data_filter: ', field)
                    # Создаем специфический фильтр для даты
                    super().append(FilterField(
                        # model_class=model_class_or_field_name,
                        field_name=field_name,
                        type='date_range',  # Новый тип для диапазона дат
                        options={
                            'start_label': f'{field.verbose_name} начало',
                            'end_label': f'{field.verbose_name} конец'
                        }
                    ))
                elif hasattr(field, 'flatchoices'):
                    options = dict(field.flatchoices)
                    super().append(FilterField(field_name, 'select', options))
                else:
                    print('field: ', field)
                    super().append(FilterField(field_name, type))
                
        except FieldDoesNotExist:
            raise ValueError(f"Поле '{field_name}' не найдено в модели.")
        except AttributeError:
            raise ValueError("Модель не распознана. Проверьте правильность аргументов.")    

     def as_dict(self):
        """
        Возвращает коллекцию фильтров в виде словаря для удобной передачи в шаблон.
        """
        return {item.field_name: {'type': item.type, 'options': item.options} for item in self}

     def sort_by_type(self):
        """
        Сортирует фильтры по типу (например, сначала text-фильтры, затем select).
        """
        self.sort(key=lambda x: x.type != 'input')

     def group_by_model(self):
        """
        Группирует фильтры по принадлежности к одной модели.
        """
        grouped = {}
        for filt in self:
            grouped.setdefault(filt.model_class.__name__, []).append(filt)
        return grouped

# Создайте собственный фильтр для форматирования чисел:



@register.filter()
def format_number(value):
    if isinstance(value, decimal.Decimal):
        return f'{value:,.2f}'.replace(',', ' ').replace('.', ',')
    elif isinstance(value, DateTimeField):
        return value.strftime('%Y-%m-%d %H:%M')
    else:
        return value


@register.filter()
def get_label(value, headers):
    for header in headers:
        if header['field'] == value:
            return header['label']



    



